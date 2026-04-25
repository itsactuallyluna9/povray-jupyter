from .magic import PovRayMagics
from .render import render


def load_ipython_extension(ipython):
    ipython.register_magics(PovRayMagics)


__all__ = ["render"]
