import io
import threading

from povray_jupyter.exceptions import (
    POVRayNotFoundError,
    POVRaySyntaxError,
    POVRayWarning,
)
import pytest
from conftest import needs_povray
from PIL import Image

from povray_jupyter.render import render_sdl, render_py_animation


@needs_povray
def test_render_valid(minimal_sdl):
    data = render_sdl(minimal_sdl)
    img = Image.open(io.BytesIO(data))
    assert img.size == (800, 600)


@needs_povray
def test_render_invalid():
    with pytest.raises(POVRaySyntaxError) as excinfo:
        render_sdl(":3")
    error_msg = str(excinfo.value)
    assert "POV-Ray failed" in error_msg
    assert "return code" in error_msg


@needs_povray
def test_render_with_warnings():
    # create SDL that generates a warning about missing assumed_gamma but still renders
    warning_sdl = """
#version 3.7;
#include "colors.inc"
// Note: NO global_settings { assumed_gamma 1.0; } - this should trigger a warning
camera { location <0,2,-3> look_at <0,1,0> }
light_source { <5,5,-5> White }
sphere { <0,1,0>, 1 pigment { color Red } }
"""

    # capture warnings
    with pytest.warns(POVRayWarning) as warning_info:
        data = render_sdl(warning_sdl)
    # verify we still got a valid image
    img = Image.open(io.BytesIO(data))
    assert img.size == (800, 600)

    # check that we got at least one warning
    assert len(warning_info.list) > 0
    warning_messages = [str(w.message) for w in warning_info.list]
    # check that at least one warning contains expected content
    assert any("POV-Ray warning:" in msg for msg in warning_messages)
    assert any("assumed_gamma" in msg for msg in warning_messages)


def test_render_fails_on_no_povray(monkeypatch):
    # remove povray from PATH by setting PATH to empty
    monkeypatch.setenv("PATH", "")

    # test SDL that would normally work
    test_sdl = """\
#version 3.7;
#include "colors.inc"
camera { location <0,2,-3> look_at <0,1,0> }
light_source { <5,5,-5> White }
sphere { <0,1,0>, 1 pigment { color Red } }
"""

    with pytest.raises(POVRayNotFoundError) as excinfo:
        render_sdl(test_sdl)

    error_msg = str(excinfo.value)
    assert "POV-Ray failed" in error_msg


@pytest.mark.skip
def test_render_py_animation_uses_concurrency(monkeypatch):
    started_second_render = threading.Event()
    call_count = 0
    call_count_lock = threading.Lock()

    def fake_render(sdl, **kwargs):
        nonlocal call_count
        with call_count_lock:
            call_count += 1
            current_call = call_count

        if current_call == 1:
            assert started_second_render.wait(timeout=1), "expected a concurrent render to start"
        else:
            started_second_render.set()

        return sdl.encode("utf-8")

    monkeypatch.setattr("povray_jupyter.render.render_sdl", fake_render)

    frames = list(
        render_py_animation(
            lambda clock: f"frame-{clock}",
            frames=2,
            concurrent_povray=2,
        )
    )

    assert frames == [b"frame-0.0", b"frame-1.0"]


@pytest.mark.skip
def test_render_py_animation_generates_while_rendering(monkeypatch):
    first_render_started = threading.Event()
    second_sdl_generated = threading.Event()

    def fake_func(clock):
        if clock == 0.0:
            return "frame-0"

        assert first_render_started.wait(timeout=1), "expected rendering to start before the next SDL"
        second_sdl_generated.set()
        return "frame-1"

    def fake_render(sdl, **kwargs):
        if sdl == "frame-0":
            first_render_started.set()
            assert second_sdl_generated.wait(timeout=1), "expected SDL generation to continue while rendering"
        return sdl.encode("utf-8")

    monkeypatch.setattr("povray_jupyter.render.render_sdl", fake_render)

    frames = list(
        render_py_animation(
            fake_func,
            frames=2,
            concurrent_povray=2,
        )
    )

    assert frames == [b"frame-0", b"frame-1"]
