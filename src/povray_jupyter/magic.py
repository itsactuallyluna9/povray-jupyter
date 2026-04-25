from IPython.core.magic import register_cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Image, display

from .render import render


@magic_arguments()
@argument("--width", type=int, default=800)
@argument("--height", type=int, default=600)
@register_cell_magic
def povray(line, cell):
    args = parse_argstring(povray, line)
    png = render(cell, width=args.width, height=args.height)
    display_png(png)


def display_png(png_bytes: bytes, embed=True):
    display(Image(data=png_bytes, format="png", embed=embed))
