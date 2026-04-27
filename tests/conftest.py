import shutil

import pytest

needs_povray = pytest.mark.skipif(
    shutil.which("povray") is None, reason="requires povray to be on path"
)


@pytest.fixture
def minimal_sdl():
    return """\
#version 3.7;
#include "colors.inc"
global_settings { assumed_gamma 1.0 }
camera { location <0,2,-3> look_at <0,1,0> }
light_source { <5,5,-5> White }
sphere { <0,1,0>, 1 pigment { color Red } }
"""
