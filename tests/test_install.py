"""Installation outputs owned by attach: cloud setup files, ignore exceptions, publication target."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rampkit import core
from rampkit.cli import attach, main

KIT = Path(__file__).resolve().parents[1]
COMMIT = ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm"]


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        (self.repo / "src").mkdir()
        (self.repo / "src/scheduler.py").write_text("class Scheduler:\n    pass\n")
        # Upstream Diffusers ignores .cursor; the installation must still be committable.
        (self.repo / ".gitignore").write_text(".cursor\n*.lock\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git(*COMMIT, "fixture")
        self.profile = {
            "base_sha": self.git("rev-parse", "HEAD").strip(),
            "upstream": "https://github.com/huggingface/diffusers.git",
            "sources": {"src/scheduler.py": core.digest((self.repo / "src/scheduler.py").read_bytes())},
            "editable_files": ["src/scheduler.py"],
            "implementation_files": ["src/scheduler.py"],
            "test_file": "src/scheduler.py",
            "upstream_checks": [],
        }
        profile_patch = patch.object(core, "profile", return_value=self.profile)
        profile_patch.start()
        self.addCleanup(profile_patch.stop)

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, check=True, capture_output=True, text=True
        ).stdout

    def test_cloud_setup_files_survive_commit_and_clone(self):
        self.assertEqual(attach(self.repo)["status"], "ATTACHED")
        for relative, template in (
            (".cursor/environment.json", "templates/cursor-environment.json"),
            (".cursor/ramp-cloud-setup.sh", "templates/ramp-cloud-setup.sh"),
        ):
            self.assertEqual((self.repo / relative).read_bytes(), (KIT / template).read_bytes())
            self.assertIn(relative, core.attachment(self.repo)["files"])
        environment = json.loads((self.repo / ".cursor/environment.json").read_text())
        self.assertEqual(environment["install"], "bash .cursor/ramp-cloud-setup.sh install")
        self.assertEqual(environment["start"], "bash .cursor/ramp-cloud-setup.sh start")
        self.git("add", "-A")
        self.git(*COMMIT, "Attach kit")
        tracked = set(self.git("ls-files").splitlines())
        self.assertTrue(set(core.attachment(self.repo)["files"]) <= tracked)
        # Other .cursor content, such as personal settings, stays ignored.
        (self.repo / ".cursor/private-settings.json").write_text("{}")
        self.assertEqual(self.git("status", "--porcelain").strip(), "")
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / "clone"
            subprocess.run(["git", "clone", "-q", str(self.repo), str(clone)], check=True)
            self.assertEqual(core.doctor(clone, dependencies=False)["status"], "PASS")

    def test_publication_target_is_recorded_and_protected(self):
        result = main(
            [
                "--repo",
                str(self.repo),
                "attach",
                "--publish-repo",
                "example-owner/diffusers",
                "--publish-base",
                "ramp-demo",
            ]
        )
        self.assertEqual(result, 0)
        record = json.loads((self.repo / ".ramp-kit/publication.json").read_text())
        self.assertEqual(record["repository"], "example-owner/diffusers")
        self.assertEqual(record["base_branch"], "ramp-demo")
        self.assertIn(".ramp-kit/publication.json", core.attachment(self.repo)["files"])
        (self.repo / ".ramp-kit/publication.json").write_text('{"repository": "huggingface/diffusers"}\n')
        self.assertEqual(core.doctor(self.repo, dependencies=False)["status"], "ERROR")

    def test_nested_publication_branch_is_accepted(self):
        attach(self.repo, "example-owner/diffusers", "team/ramp-demo")
        record = json.loads((self.repo / ".ramp-kit/publication.json").read_text())
        self.assertEqual(record["base_branch"], "team/ramp-demo")

    def test_publication_target_without_flags_is_absent(self):
        attach(self.repo)
        self.assertFalse((self.repo / ".ramp-kit/publication.json").exists())

    def test_invalid_publication_targets_change_nothing(self):
        for repository, base, message in (
            ("example-owner/diffusers", None, "Name both"),
            (None, "ramp-demo", "Name both"),
            ("huggingface/diffusers", "main", "not the upstream project"),
            ("HuggingFace/Diffusers", "main", "not the upstream project"),
            ("not a repository", "ramp-demo", "OWNER/NAME"),
            ("example-owner/diffusers", "bad..branch", "valid branch name"),
            # Each of these is rejected by `git check-ref-format --branch`.
            ("example-owner/diffusers", ".", "valid branch name"),
            ("example-owner/diffusers", "/ramp-demo", "valid branch name"),
            ("example-owner/diffusers", "ramp-demo/", "valid branch name"),
            ("example-owner/diffusers", "foo.lock", "valid branch name"),
            ("example-owner/diffusers", "-ramp-demo", "valid branch name"),
            ("example-owner/diffusers", "@{-1}", "valid branch name"),
            ("example-owner/diffusers", "HEAD", "valid branch name"),
            ("example-owner/diffusers", "ramp demo", "valid branch name"),
        ):
            with self.subTest(repository=repository, base=base):
                with self.assertRaisesRegex(core.RampError, message):
                    attach(self.repo, repository, base)
                self.assertFalse((self.repo / ".ramp-kit").exists())
                self.assertFalse((self.repo / ".cursor").exists())


class CloudSetupScriptTests(unittest.TestCase):
    script = KIT / "templates/ramp-cloud-setup.sh"

    def run_script(self, repo: Path, phase: str):
        return subprocess.run(["bash", str(self.script), phase], cwd=repo, capture_output=True, text=True)

    def fresh_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        return repo

    def test_legacy_ramp_kit_path_refuses_both_phases(self):
        repo = self.fresh_repo()
        (repo / "ramp-kit").mkdir()
        for phase in ("install", "start"):
            with self.subTest(phase=phase):
                result = self.run_script(repo, phase)
                self.assertEqual(result.returncode, 2)
                self.assertIn("legacy ramp-kit path", result.stderr)
                self.assertIn("fresh Cursor environment", result.stderr)

    def test_branch_without_installation(self):
        repo = self.fresh_repo()
        self.assertEqual(self.run_script(repo, "install").returncode, 0)
        result = self.run_script(repo, "start")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no Ramp Kit installation", result.stderr)

    def test_unknown_phase(self):
        result = self.run_script(self.fresh_repo(), "deploy")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Expected install or start", result.stderr)


if __name__ == "__main__":
    unittest.main()
