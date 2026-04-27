from .magic import PovRayMagics, display_png
from .render import render


def load_ipython_extension(ipython):
    ipython.register_magics(PovRayMagics)


__all__ = ["render", "display_png"]
