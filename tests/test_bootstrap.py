"""Interpreter-routing and error-path tests; not substitutes for a cold install."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class BootstrapTests(unittest.TestCase):
    def test_default_interpreter_and_missing_venv_diagnostic(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / "python3.12"
            stub.write_text(
                '#!/bin/sh\n[ "$1" = "-c" ] && exit 0\n[ "$1" = "-m" ] && [ "$2" = "venv" ] && exit 1\nexit 99\n'
            )
            stub.chmod(0o755)
            (root / "python3").write_text("#!/bin/sh\nexit 99\n")
            (root / "python3").chmod(0o755)
            env = {**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]}
            env.pop("PYTHON", None)
            result = subprocess.run(["bash", str(script), str(root)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Install python3.12-venv", result.stderr)
            self.assertIn("virtualenv", result.stderr)

    def test_missing_ensurepip_falls_back_to_venv_without_pip(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calls = root / "calls.log"
            stub = root / "python3.12"
            # Plain venv fails (no ensurepip); venv --without-pip and the interpreter's pip work.
            stub.write_text(
                "#!/bin/sh\n"
                f'echo "$@" >> "{calls}"\n'
                '[ "$1" = "-c" ] && exit 0\n'
                'if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then\n'
                '  [ "$3" = "--without-pip" ] || exit 1\n'
                '  mkdir -p "$4/bin"; printf "#!/bin/sh\\nexit 0\\n" > "$4/bin/python"; chmod +x "$4/bin/python"; exit 0\n'
                "fi\n"
                '[ "$1" = "-m" ] && [ "$2" = "pip" ] && [ "$3" = "--python" ] && exit 0\n'
                "exit 99\n"
            )
            stub.chmod(0o755)
            env = {**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]}
            env.pop("PYTHON", None)
            result = subprocess.run(["bash", str(script), str(root)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("no ensurepip", result.stderr)
            self.assertIn("--without-pip", calls.read_text())
            self.assertTrue((root / ".ramp-venv/.gitignore").is_file())

    def venv_stub(self, root: Path) -> dict:
        """A python3.12 whose plain venv works and creates a usable environment."""
        stub = root / "python3.12"
        stub.write_text(
            "#!/bin/sh\n"
            '[ "$1" = "-c" ] && exit 0\n'
            'if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then\n'
            '  mkdir -p "$3/bin"; : > "$3/pyvenv.cfg"\n'
            '  printf "#!/bin/sh\\nexit 0\\n" > "$3/bin/python"; chmod +x "$3/bin/python"; exit 0\n'
            "fi\n"
            "exit 99\n"
        )
        stub.chmod(0o755)
        env = {**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]}
        env.pop("PYTHON", None)
        return env

    def test_unrecognised_environment_directory_is_preserved(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sentinel = root / ".ramp-venv/notes.txt"
            sentinel.parent.mkdir()
            sentinel.write_text("not an environment")
            result = subprocess.run(
                ["bash", str(script), str(root)], env=self.venv_stub(root), capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("not a Python environment", result.stderr)
            self.assertIn("nothing was removed", result.stderr)
            self.assertEqual(sentinel.read_text(), "not an environment")

    def test_symlinked_environment_is_not_replaced(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "elsewhere"
            target.mkdir()
            (target / "pyvenv.cfg").write_text("")
            (root / ".ramp-venv").symlink_to(target)
            result = subprocess.run(
                ["bash", str(script), str(root)], env=self.venv_stub(root), capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("symbolic link", result.stderr)
            self.assertTrue((root / ".ramp-venv").is_symlink())
            self.assertTrue((target / "pyvenv.cfg").is_file())

    def test_broken_managed_environment_is_replaced(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".ramp-venv").mkdir()
            (root / ".ramp-venv/pyvenv.cfg").write_text("")  # Environment without a usable interpreter.
            result = subprocess.run(
                ["bash", str(script), str(root)], env=self.venv_stub(root), capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(os.access(root / ".ramp-venv/bin/python", os.X_OK))

    def test_explicit_missing_interpreter_has_actionable_message(self):
        script = Path(__file__).resolve().parents[1] / "runtime/bootstrap.sh"
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                ["bash", str(script), tmp],
                env={**os.environ, "PYTHON": "/missing/python3.12"},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("set PYTHON", result.stderr)
