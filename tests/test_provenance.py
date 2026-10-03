"""Fork CI provenance: which revisions were verified, by which kit, with which patch digest."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from rampkit import core

KIT = Path(__file__).resolve().parents[1]
SCRIPT = KIT / "runtime/ci_provenance.py"
COMMIT = ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm"]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.pin = json.loads((KIT / "profiles/diffusers.json").read_text())["base_sha"]

        # Policy: the PR base with the installed kit, as the workflow checks it out.
        self.policy = root / "policy"
        installed = self.policy / ".ramp-kit"
        for folder in ("rampkit", "profiles", "recipes", "cursor", "templates", "examples", "runtime"):
            shutil.copytree(KIT / folder, installed / folder, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(KIT / "run.py", installed / "run.py")
        self.kit_sha = core.kit_hash(KIT)
        (installed / "attachment.json").write_text(json.dumps({"kit_sha256": self.kit_sha, "files": {}}))
        git(root, "init", "-q", str(self.policy))
        git(self.policy, "add", "-A")
        git(self.policy, *COMMIT, "base installation")
        self.base = git(self.policy, "rev-parse", "HEAD")

        # Candidate: GitHub's merge of the PR head into the base.
        self.candidate = root / "candidate"
        subprocess.run(["git", "clone", "-q", str(self.policy), str(self.candidate)], check=True)
        git(self.candidate, "switch", "-q", "-c", "contribution")
        (self.candidate / "change.txt").write_text("contribution\n")
        git(self.candidate, "add", "change.txt")
        git(self.candidate, *COMMIT, "contribution")
        self.head = git(self.candidate, "rev-parse", "HEAD")
        git(self.candidate, "switch", "-q", "--detach", self.base)
        git(self.candidate, *COMMIT[:4], "merge", "-q", "--no-ff", "--no-edit", self.head)
        self.merge = git(self.candidate, "rev-parse", "HEAD")
        record = {
            "status": "PASS",
            "level": "full",
            "base_sha": self.pin,
            "patch_sha256": "ab" * 32,
            "policy": {"runner_kit_sha256": self.kit_sha, "installation_kit_sha256": self.kit_sha},
        }
        (self.candidate / ".ramp/zero-steps").mkdir(parents=True)
        (self.candidate / ".ramp/zero-steps/candidate.json").write_text(json.dumps(record))
        self.output = root / "out/ci-provenance.json"
        self.env = {
            **os.environ,
            "GITHUB_REPOSITORY": "example-owner/diffusers",
            "GITHUB_REF": "refs/pull/7/merge",
            "GITHUB_RUN_ID": "123",
            "GITHUB_RUN_ATTEMPT": "2",
            "GITHUB_WORKFLOW": "Ramp Kit contribution checks",
            "RAMP_PR_NUMBER": "7",
            "RAMP_PR_BASE_SHA": self.base,
            "RAMP_PR_HEAD_SHA": self.head,
        }

    def run_script(self, env=None):
        result = subprocess.run(
            [
                "python3",
                str(self.policy / ".ramp-kit/runtime/ci_provenance.py"),
                "--policy",
                str(self.policy),
                "--candidate",
                str(self.candidate),
                "--output",
                str(self.output),
            ],
            env=env or self.env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(self.output.read_text())

    def test_records_every_agreed_field(self):
        record = self.run_script()
        self.assertEqual(record["upstream_pin"], self.pin)
        self.assertEqual(record["pr_base_sha"], self.base)
        self.assertEqual(record["pr_head_sha"], self.head)
        self.assertEqual(record["tested_checkout_sha"], self.merge)
        self.assertEqual(set(record["tested_checkout_parents"]), {self.base, self.head})
        self.assertEqual(record["policy_checkout_sha"], self.base)
        self.assertEqual((record["run_id"], record["run_attempt"]), ("123", "2"))
        self.assertEqual(record["tested_ref"], "refs/pull/7/merge")
        self.assertEqual(record["runner_kit_sha256"], self.kit_sha)
        self.assertEqual(record["policy_installed_kit_sha256"], self.kit_sha)
        self.assertEqual(record["tasks"][0]["task"], "zero-steps")
        self.assertEqual(record["tasks"][0]["patch_sha256"], "ab" * 32)
        self.assertTrue(all(record["consistency"].values()), record["consistency"])
        self.assertIn("same pin", record["comparison_contract"])

    def test_inconsistent_revisions_are_reported_not_hidden(self):
        env = {**self.env, "RAMP_PR_BASE_SHA": "0" * 40, "RAMP_PR_HEAD_SHA": "1" * 40}
        consistency = self.run_script(env)["consistency"]
        self.assertFalse(consistency["policy_checkout_is_pr_base"])
        self.assertFalse(consistency["tested_checkout_contains_pr_head"])

    def test_failed_or_missing_verification_still_records_revisions(self):
        shutil.rmtree(self.candidate / ".ramp")
        record = self.run_script()
        self.assertEqual(record["tasks"], [])
        self.assertEqual(record["tested_checkout_sha"], self.merge)
        # Absent task evidence must never read as consistent task evidence.
        self.assertFalse(record["consistency"]["task_patches_use_upstream_pin"])

    def test_workflow_runs_recorder_from_policy_after_verification(self):
        workflow = (KIT / "templates/fork-ci.yml").read_text()
        step = workflow.split("- name: Record which revisions were verified", 1)[1].split("- uses:", 1)[0]
        self.assertIn("if: always()", step)
        self.assertIn("python policy/.ramp-kit/runtime/ci_provenance.py --policy policy", step)
        for name in ("RAMP_PR_BASE_SHA", "RAMP_PR_HEAD_SHA", "RAMP_PR_NUMBER"):
            self.assertIn(f"{name}: ${{{{ github.event.pull_request.", step)
        self.assertLess(workflow.index("Verify each task"), workflow.index("Record which revisions"))
        self.assertLess(workflow.index("Record which revisions"), workflow.index("upload-artifact"))
        self.assertTrue(SCRIPT.is_file())


if __name__ == "__main__":
    unittest.main()
