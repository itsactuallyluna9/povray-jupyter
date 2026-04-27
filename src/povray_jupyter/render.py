import subprocess
import tempfile
import warnings
from pathlib import Path


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
            raise RuntimeError("POV-Ray failed: povray executable not found in PATH")

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
                warnings.warn(f"POV-Ray warning: {line.strip()}", UserWarning)

        if result.returncode != 0 or not output_file.exists():
            error_msg = f"POV-Ray failed with return code {result.returncode}."
            if result.stderr:
                error_msg += f" stderr: {result.stderr.strip()}"
            if result.stdout:
                error_msg += f" stdout: {result.stdout.strip()}"
            raise RuntimeError(error_msg)

        return output_file.read_bytes()
