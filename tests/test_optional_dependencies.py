"""Test that seekpath works without its optional dependencies."""

import subprocess
import sys
import unittest

# Make every import of scipy fail, as if it were not installed
BLOCK_SCIPY = "import sys; sys.modules['scipy'] = None; "


def run_python(code):
    """Run ``code`` in a fresh interpreter, so no module is imported yet."""
    return subprocess.run(
        [sys.executable, '-c', code], capture_output=True, text=True, check=False
    )


class TestWithoutScipy(unittest.TestCase):
    """seekpath only needs scipy for the Brillouin zone subpackage."""

    def test_get_path_without_scipy(self):
        """``import seekpath`` and ``get_path`` must not need scipy."""
        result = run_python(
            BLOCK_SCIPY + 'import seekpath; '
            'print(seekpath.get_path(([[4.0, 0, 0], [0, 4.0, 0], [0, 0, 4.0]], '
            "[[0, 0, 0]], [1]))['bravais_lattice'])"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'cP')

    def test_brillouinzone_without_scipy(self):
        """The Brillouin zone subpackage explains how to install scipy."""
        result = run_python(BLOCK_SCIPY + 'import seekpath; seekpath.brillouinzone')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ImportError', result.stderr)
        self.assertIn('pip install seekpath[bz]', result.stderr)


class TestBrillouinzoneAccess(unittest.TestCase):
    """The Brillouin zone subpackage is reachable in all the supported ways."""

    def test_access_paths_agree(self):
        """``seekpath.brillouinzone.BZ`` is the same class however it is reached."""
        result = run_python(
            'import seekpath; '
            'from seekpath.brillouinzone import brillouinzone; '
            'from seekpath.brillouinzone import BZ; '
            'print(seekpath.brillouinzone.BZ is brillouinzone.BZ is BZ)'
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'True')

    def test_unknown_attribute(self):
        """Other missing attributes still raise ``AttributeError``."""
        import seekpath

        with self.assertRaises(AttributeError):
            seekpath.not_an_attribute  # noqa: B018


if __name__ == '__main__':
    unittest.main()
