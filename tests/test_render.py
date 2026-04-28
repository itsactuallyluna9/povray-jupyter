import io

from povray_jupyter.exceptions import (
    POVRayNotFoundError,
    POVRaySyntaxError,
    POVRayWarning,
)
import pytest
from conftest import needs_povray
from PIL import Image

from povray_jupyter.render import render


@needs_povray
def test_render_valid(minimal_sdl):
    data = render(minimal_sdl)
    img = Image.open(io.BytesIO(data))
    assert img.size == (800, 600)


@needs_povray
def test_render_invalid():
    with pytest.raises(POVRaySyntaxError) as excinfo:
        render(":3")
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
        data = render(warning_sdl)
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
        render(test_sdl)

    error_msg = str(excinfo.value)
    assert "POV-Ray failed" in error_msg
