"""scipy is only needed for the Brillouin zone (the `bz` extra)."""

import subprocess
import sys


def test_import_without_scipy():
    """`import seekpath` must work when scipy is not installed."""
    code = "import sys; sys.modules['scipy'] = None; import seekpath"
    subprocess.run([sys.executable, '-c', code], check=True)
