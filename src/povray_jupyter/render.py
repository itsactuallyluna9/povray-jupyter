import subprocess
import tempfile
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
            "+FN",
            f"+O{output_file}",
            "-D",
            "+UA",
            f"+A{'0.3' if antialias else ''}",
            str(scene_file),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise RuntimeError("POV-Ray failed :(")

        return output_file.read_bytes()
