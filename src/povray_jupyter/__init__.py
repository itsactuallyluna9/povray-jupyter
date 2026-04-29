from .magic import PovRayMagics, display_png
from .render import render_sdl
import warnings as _warnings

def render(sdl: str, width=800, height=600, antialias=True):
    _warnings.warn("povray_jupyter.render() is deprecated, use render_sdl() instead", DeprecationWarning, stacklevel=2)
    return render_sdl(sdl, width=width, height=height, antialias=antialias)

def load_ipython_extension(ipython):
    ipython.register_magics(PovRayMagics)


__all__ = ["render_sdl", "display_png"]
