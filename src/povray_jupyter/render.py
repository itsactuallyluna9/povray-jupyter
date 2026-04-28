import subprocess
import tempfile
from typing import Iterable
import warnings
from pathlib import Path
import re

from povray_jupyter.exceptions import POVRayNotFoundError, POVRayRuntimeError, POVRaySyntaxError, POVRaySyntaxWarning, POVRayWarning


def render(sdl: str, width=800, height=600, antialias=True) -> bytes:
    with tempfile.TemporaryDirectory(prefix="jupyter-povray") as tempdir:
        scene_file = Path(tempdir) / "scene.pov"
        output_file = Path(tempdir) / "output.png"

        scene_file.write_text(sdl)

        cmd = [
            "povray",
            f"+W{width}",
            f"+H{height}",
            "+FN",  # ?
            f"+O{output_file}",
            "-D",  # don't display anything
            "+UA",  # output alpha
            f"+A{'0.3' if antialias else ''}",
            str(scene_file),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            # povray executable not found in PATH
            raise POVRayNotFoundError("POV-Ray failed: povray executable not found in PATH")

        # check for warnings in output and issue them
        full_output = result.stdout + result.stderr
        for line in full_output.splitlines():
            line_lower = line.lower()
            # skip informational lines about POV-Ray configuration
            if "warning stream to console" in line_lower:
                continue
            # warn for actual warning messages - look for lines that contain warning indicators
            # but are not just informational
            if "warning" in line_lower and (
                "parse warning" in line_lower
                or "possible parse error" in line_lower
                or line_lower.strip().startswith("warning")
                or ("this warning" in line_lower and "explicitly specify" in line_lower)
            ):
                warnings.warn(f"POV-Ray warning: {line.strip()}", POVRayWarning)
                # warnings.warn_explicit(f"POV-Ray warning: {line.strip()}", category=POVRaySyntaxWarning, filename=str(scene_file), lineno=0)

        if result.returncode != 0 or not output_file.exists():
            if "parse error" in full_output.lower():
                # alright: we gotta parse error - let's try to extract the line number and message
                # 3.6:
                # File: /tmp/jupyter-povray_e7l35_e/scene.pov  Line: 4
                # File Context (5 lines):
                # #include "colors.inc"
                # camera { location <0,2,-3> look_at <0,1,0> }
                # light_source { <5,5,-5> White }
                # sphere { <0,1,0>, 1 pigment { color White }
                #
                # Parse Error: No matching } in 'sphere', End of File found instead

                # 3.7:
                # File 'test.pov' line 10: Parse Error: No matching } in 'light_source', sphere
                # found instead
                # Fatal error in parser: Cannot parse input

                parse_error_match = re.search(r"File[: ]\s*['\"]?(.+?)['\"]?\s*line[: ]\s*(\d+)", full_output, re.IGNORECASE)
                if parse_error_match:
                    error_file = parse_error_match.group(1)
                    error_line = int(parse_error_match.group(2))
                    error_msg = f"POV-Ray syntax error in file '{error_file}' at line {error_line} - check the stderr and stdout for details."
                    if result.stderr:
                        error_msg += f" stderr: {result.stderr.strip()}"
                    if result.stdout:
                        error_msg += f" stdout: {result.stdout.strip()}"
                    error = POVRaySyntaxError(error_msg)
                    error.filename = error_file
                    error.lineno = error_line
                    error.text = scene_file.read_text().splitlines()[error_line - 1] 
                    raise error
            else:
                error_msg = f"POV-Ray failed with return code {result.returncode} - check the stderr and stdout for details."
                if result.stderr:
                    error_msg += f" stderr: {result.stderr.strip()}"
                if result.stdout:
                    error_msg += f" stdout: {result.stdout.strip()}"
                raise POVRayRuntimeError(error_msg)

        return output_file.read_bytes()

def render_pov_animation(sdl: str, frames=60, infinite=False, **kwargs) -> Iterable[bytes]:
    """
    Render an animation using POV-Ray's built-in animation features.
    
    This will set the CLOCK variable to 0.0, and then increment it up to 1.0 across the specified number of frames.

    Please see the POV-Ray documentation for details on how to use the CLOCK variable to create animations:
    https://www.povray.org/documentation/3.7.0/r3_2.html#r3_2_1

    Arguments:
    - sdl: The SDL string for the scene, which should use the CLOCK variable to create animation effects.
    - frames: The number of frames to render for the animation.
    - infinite: If True, the animation's frames will be setup to loop infinitely.
    """
    raise NotImplementedError("Animation rendering is not yet implemented.")

def render_py_animation(func, frames=60, infinite=False) -> Iterable[bytes]:
    """
    Render an animation by calling a Python function that generates the SDL for each frame. The function should take a single argument (the current time/frame) and return the SDL string for that frame.

    This will call the provided function with a time value that goes from 0.0 to 1.0 across the specified number of frames, and then render each frame using the render() function. This mirrors the behavior of render_pov_animation, but allows you to generate the SDL dynamically in Python rather than relying on POV-Ray's built-in animation features.
    For simplicity's sake, the CLOCK variable will also be set when using this function.
    """
    for frame in range(frames):
        time = frame / (frames - 1) if frames > 1 else 0
        sdl = func(time)

    raise NotImplementedError("Animation rendering is not yet implemented.")
