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
