import io

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
    with pytest.raises(Exception) as excinfo:
        render(":3")


@pytest.mark.skip
def test_render_fails_on_no_povray(minimal_sdl):
    # TODO: we need to remove PATH to properly test this...
    render(minimal_sdl)
