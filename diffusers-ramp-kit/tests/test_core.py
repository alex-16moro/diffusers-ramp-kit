import contextlib
import copy
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rampkit import core
from rampkit.cli import attach, main, onboard
from rampkit.report import render


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.source = "src/scheduler.py"
        self.tests = "tests/test_scheduler.py"
        (self.repo / "src").mkdir()
        (self.repo / "tests").mkdir()
        (self.repo / self.source).write_text("class Scheduler:\n    def step(self):\n        return 1\n")
        (self.repo / self.tests).write_text("# initial tests\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git(
            "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"
        )
        self.sha = self.git("rev-parse", "HEAD").strip()
        self.profile = {
            "base_sha": self.sha,
            "sources": {
                name: core.digest((self.repo / name).read_bytes()) for name in [self.source, self.tests]
            },
            "editable_files": [self.source, self.tests],
            "implementation_files": [self.source],
            "test_file": self.tests,
            "upstream_checks": [],
        }
        self.task = {
            "id": "task",
            "title": "Validation",
            "request": "Reject empty input",
            "base_sha": self.sha,
            "recipe": "scheduler-input-validation",
            "editable_files": [self.source, self.tests],
            "regression_test": self.tests + "::Tests::test_empty",
            "criteria": [
                {"id": "AC1", "text": "Raises ValueError", "tests": [self.tests + "::Tests::test_empty"]}
            ],
        }
        self.prof_patch = patch.object(core, "profile", return_value=self.profile)
        self.prof_patch.start()
        self.addCleanup(self.prof_patch.stop)
        self.directory = core.task_dir(self.repo, "task")
        core.write(self.directory / "task.json", self.task)
        core.write(
            self.directory / "architecture.json",
            {"decision": "COMPATIBLE", "task_sha256": core.digest(core.canonical(self.task))},
        )

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args], text=True, stderr=subprocess.DEVNULL
        )

    def test_traversal_rejected(self):
        for path in ["../secret", "/etc/passwd", "src/../../other"]:
            with self.assertRaises(core.RampError):
                core.safe_path(self.repo, path)

    def test_symlink_rejected(self):
        (self.repo / "alias").symlink_to(self.repo / "src", target_is_directory=True)
        with self.assertRaises(core.RampError):
            core.safe_path(self.repo, "alias/scheduler.py")

    def test_context_allowlist_and_symbol(self):
        with self.assertRaises(core.RampError):
            core.context(self.repo, ".env")
        result = core.context(self.repo, self.source, "Scheduler.step")
        self.assertIn("return 1", result["content"])
        with self.assertRaises(core.RampError):
            core.context(self.repo, self.source, "Scheduler.missing")

    def test_invalid_base_never_means_no_changes(self):
        with self.assertRaises(core.RampError):
            core.changed(self.repo, "invalid-base")

    def test_deletion_detected(self):
        (self.repo / self.source).unlink()
        self.assertIn(self.source, core.changed(self.repo, self.sha))
        self.assertTrue(any("Deleting" in f["message"] for f in core.scope_findings(self.repo, self.task)))

    def test_untracked_out_of_scope_detected(self):
        (self.repo / "unrelated.py").write_text("pass\n")
        self.assertEqual(core.scope_findings(self.repo, self.task)[0]["rule"], "SCOPE")

    def test_existing_test_filename_selected(self):
        (self.repo / self.tests).write_text("# changed existing test_scheduler file\n")
        self.assertIn(self.tests, core.changed(self.repo, self.sha))
        self.assertFalse(core.scope_findings(self.repo, self.task))

    def test_task_cannot_choose_shell_as_test(self):
        self.task["criteria"][0]["tests"] = ["--override-ini=anything"]
        with self.assertRaises(core.RampError):
            core.validate_task(self.task, self.profile)

    def test_unmapped_acceptance_criterion_rejected(self):
        self.task["criteria"][0]["tests"] = []
        with self.assertRaises(core.RampError):
            core.validate_task(self.task, self.profile)

    def test_evidence_changes_with_code_and_requirement(self):
        first = core.fingerprint(self.repo, self.task)
        (self.repo / self.source).write_text("# changed\n")
        self.assertNotEqual(first, core.fingerprint(self.repo, self.task))
        second = core.fingerprint(self.repo, self.task)
        self.task["request"] = "A different outcome"
        self.assertNotEqual(second, core.fingerprint(self.repo, self.task))

    def test_old_green_report_is_stale(self):
        core.write(self.directory / "candidate.json", {"fingerprint": "old", "status": "PASS"})
        self.assertEqual(core.readiness(self.repo, self.task)["status"], "STALE")

    def test_source_drift_reported(self):
        self.profile["sources"][self.source] = "wrong"
        result = core.doctor(self.repo, dependencies=False)
        self.assertEqual(result["status"], "ERROR")
        self.assertTrue(any("mismatch" in f for f in result["findings"]))

    def test_pushback_needs_evidence_and_alternative(self):
        with self.assertRaises(core.RampError):
            core.assess(
                self.repo,
                "task",
                "REVISE",
                "This proposal changes valid behaviour unexpectedly.",
                [self.source],
                "",
            )
        result = core.assess(
            self.repo,
            "task",
            "REVISE",
            "This proposal changes valid behaviour unexpectedly.",
            [self.source],
            "Keep validation at the owning API.",
        )
        self.assertEqual(result["kind"], "agent_assessment_not_human_approval")

    def test_broad_exception_swallowing_diagnostic(self):
        fixture = Path(__file__).parent / "fixtures/broad_exception.txt"
        (self.repo / self.source).write_text(fixture.read_text())
        self.assertEqual(core.diagnostic(self.repo, self.task)[0]["rule"], "NO-SILENT-FALLBACK")

    def test_skipped_test_never_passes(self):
        def fake(repo, directory, name, argv):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{name}.xml").write_text(
                '<testsuites><testsuite><testcase name="test_a" classname="Tests"><skipped message="missing torch"/></testcase></testsuite></testsuites>'
            )
            return {"status": "PASS", "exit_code": 0}

        with patch.object(core, "run_check", side_effect=fake):
            result = core.pytest_check(self.repo, self.directory / "logs", "acceptance", [self.tests])
        self.assertEqual(result["status"], "SKIPPED")

    def test_missing_test_report_is_execution_error(self):
        with patch.object(core, "run_check", return_value={"status": "FAIL", "exit_code": 4}):
            result = core.pytest_check(self.repo, self.directory, "missing", [self.tests])
        self.assertEqual(result["status"], "ERROR")

    def test_pending_design_stops_execution(self):
        core.write(self.directory / "architecture.json", {"decision": "PENDING"})
        with (
            patch.object(core, "doctor", return_value={"status": "PASS", "runtime": {}}),
            patch.object(core, "pytest_check") as check,
        ):
            result = core.verify(self.repo, "task", "fast", "candidate")
        self.assertEqual(result["status"], "FAIL")
        check.assert_not_called()

    def test_task_cannot_replace_pinned_base(self):
        self.task["base_sha"] = "0" * 40
        with self.assertRaises(core.RampError):
            core.validate_task(self.task, self.profile)

    def test_preexisting_anti_pattern_is_not_new_finding(self):
        code = "try:\n    work()\nexcept Exception:\n    pass\n"
        (self.repo / self.source).write_text(code)
        self.git("add", self.source)
        self.git(
            "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"
        )
        self.task["base_sha"] = self.git("rev-parse", "HEAD").strip()
        self.assertEqual(core.diagnostic(self.repo, self.task), [])
        with (self.repo / self.source).open("a") as f:
            f.write(code)
        self.assertEqual(len(core.diagnostic(self.repo, self.task)), 1)

    def test_report_marks_all_prior_checks_stale(self):
        core.write(
            self.directory / "candidate.json",
            {
                "fingerprint": "old",
                "status": "PASS",
                "checks": [
                    {
                        "id": "lint",
                        "status": "PASS",
                        "seconds": 1,
                        "log": ".ramp/task/runs/old/lint.log",
                        "command": ["lint"],
                        "exit_code": 0,
                    }
                ],
            },
        )
        result = render(self.repo, "task")
        self.assertEqual(result["status"], "STALE")
        self.assertNotIn("| lint | PASS", (self.directory / "review.md").read_text())
        self.assertIn("| lint | STALE", (self.directory / "review.md").read_text())
        self.assertIn("- lint: STALE", (self.directory / "PR-DRAFT.md").read_text())

    def test_attach_idempotence_and_tamper_detection(self):
        self.assertEqual(attach(self.repo)["status"], "ATTACHED")
        self.assertEqual(attach(self.repo)["status"], "ALREADY_ATTACHED")
        (self.repo / ".cursor/rules/ramp-entry.mdc").write_text("changed")
        self.assertEqual(core.doctor(self.repo, dependencies=False)["status"], "ERROR")
        with self.assertRaises(core.RampError):
            attach(self.repo)

    def test_fresh_onboarding_excludes_solution_and_credentials(self):
        (self.repo / ".env").write_text("HARMLESS_SENTINEL=not-a-secret\n")
        (self.repo / "completed.patch").write_text("untracked solution sentinel")
        self.profile["upstream"] = "https://github.com/huggingface/diffusers.git"
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "onboarding"
            result = onboard(self.repo, destination)
            self.assertEqual(result["status"], "ONBOARDING_READY")
            self.assertFalse((destination / ".env").exists())
            self.assertFalse((destination / "completed.patch").exists())
            self.assertFalse((destination / ".ramp").exists())
            self.assertTrue((destination / ".cursor/rules/ramp-entry.mdc").exists())

    def test_regression_trace_must_reach_implementation(self):
        check = {
            "exit_code": 1,
            "tests": [{"status": "FAIL", "detail": "AssertionError: expected IndexError"}],
        }
        self.assertFalse(core.expected_regression(check, self.task))
        check["tests"][0]["detail"] = "IndexError: list index out of range\n" + self.source
        self.assertTrue(core.expected_regression(check, self.task))

    def test_mapped_test_cannot_be_missing_from_successful_result(self):
        def fake(repo, directory, name, argv):
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{name}.xml").write_text(
                '<testsuites><testsuite><testcase name="test_other" classname="Tests"/></testsuite></testsuites>'
            )
            return {"status": "PASS", "exit_code": 0}

        with patch.object(core, "run_check", side_effect=fake):
            result = core.pytest_check(
                self.repo, self.directory / "logs", "acceptance", [self.task["regression_test"]]
            )
        self.assertEqual(result["status"], "ERROR")

    def test_normal_commit_and_clone_preserves_entire_attachment(self):
        (self.repo / ".gitignore").write_text(".cursor\n*.lock\n")
        result = attach(self.repo)
        self.assertEqual(result["status"], "ATTACHED")
        self.git("add", "-A")
        self.git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "Attach kit",
        )
        tracked = set(self.git("ls-files").splitlines())
        manifest = core.attachment(self.repo)
        self.assertTrue(set(manifest["files"]) <= tracked)
        self.assertIn(".ramp-kit/runtime/requirements.txt", tracked)
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / "clone"
            subprocess.run(["git", "clone", "-q", str(self.repo), str(clone)], check=True)
            self.assertEqual(core.doctor(clone, dependencies=False)["status"], "PASS")
            (clone / ".cursor/private-settings.json").write_text("{}")
            self.assertNotIn(".cursor/private-settings.json", core.changed(clone, self.sha))

    def test_scaffold_uses_task_mappings_and_deduplicates(self):
        task = copy.deepcopy(self.task)
        task["criteria"].append(
            {"id": "AC2", "text": "Second", "tests": [self.tests + "::OtherTests::test_second"]}
        )
        scaffold = core.test_scaffold(task)
        self.assertIn("class OtherTests:", scaffold)
        self.assertIn("def test_second(self):", scaffold)
        self.assertNotIn("DDPM", scaffold)
        self.assertIn("NotImplementedError", scaffold)

    def test_empty_and_raise_only_mapped_tests_are_rejected(self):
        fixture = Path(__file__).parent / "fixtures/no_assertions.txt"
        (self.repo / self.tests).write_text(fixture.read_text())
        self.assertEqual(core.assertion_findings(self.repo, self.task)[0]["rule"], "TEST-ASSERTIONS")
        for body in ["raise ValueError('not an assertion')", "def helper():\n            assert True"]:
            (self.repo / self.tests).write_text(
                "class Tests:\n    def test_empty(self):\n        " + body + "\n"
            )
            self.assertTrue(core.assertion_findings(self.repo, self.task))

    def test_supported_assertion_patterns(self):
        for body in [
            "assert answer == 1",
            "self.assertEqual(answer, 1)",
            "with self.assertRaises(ValueError):\n            operation()",
            "with pytest.raises(ValueError):\n            operation()",
        ]:
            (self.repo / self.tests).write_text(
                "class Tests:\n    def test_empty(self):\n        " + body + "\n"
            )
            self.assertEqual(core.assertion_findings(self.repo, self.task), [])

    def test_assertion_free_candidate_cannot_reach_ready(self):
        (self.repo / self.tests).write_text("class Tests:\n    def test_empty(self):\n        pass\n")
        with (
            patch.object(core, "doctor", return_value={"status": "PASS", "runtime": {}}),
            patch.object(core, "pytest_check") as run,
        ):
            result = core.verify(self.repo, "task", "full", "candidate")
        self.assertEqual(result["status"], "FAIL")
        run.assert_not_called()
        self.assertEqual(core.readiness(self.repo, self.task)["status"], "FAIL")

    def test_patch_digest_ignores_git_display_configuration(self):
        (self.repo / self.source).write_text("class Scheduler:\n    def step(self):\n        return 2\n")
        before = core.patch_bytes(self.repo, self.task)
        self.git("config", "core.abbrev", "12")
        self.git("config", "diff.noprefix", "true")
        self.git("config", "diff.context", "9")
        self.git("config", "diff.algorithm", "histogram")
        self.assertEqual(before, core.patch_bytes(self.repo, self.task))

    def test_baseline_failure_reasons_and_exit_contract(self):
        (self.repo / self.tests).write_text("class Tests:\n    def test_empty(self):\n        assert True\n")
        cases = [
            ("PASS", 0, "", "observed PASS", "FAIL"),
            ("SKIPPED", 0, "", "observed SKIPPED", "FAIL"),
            ("FAIL", 1, "AssertionError: wrong", "observed AssertionError, expected IndexError", "FAIL"),
            ("ERROR", 2, "ImportError: missing", "REGRESSION_EXECUTION_ERROR", "ERROR"),
        ]
        for observed, exit_code, detail, reason, status in cases:
            check = {
                "id": "regression",
                "status": observed,
                "exit_code": exit_code,
                "tests": [{"status": observed, "detail": detail}],
            }
            with (
                patch.object(core, "doctor", return_value={"status": "PASS", "runtime": {}}),
                patch.object(core, "pytest_check", return_value=check),
            ):
                result = core.verify(self.repo, "task", "fast", "baseline")
            self.assertEqual(result["status"], status)
            self.assertIn(reason, result["next_action"])
        (self.directory / "architecture.json").unlink()
        with (
            patch.object(core, "doctor", return_value={"status": "PASS", "runtime": {}}),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            code = main(["--repo", str(self.repo), "verify", "task", "--phase", "baseline"])
        self.assertEqual(code, 1)

    def test_replay_does_not_overwrite_preimplementation_record(self):
        (self.repo / self.tests).write_text("class Tests:\n    def test_empty(self):\n        assert True\n")
        baseline = {"status": "EXPECTED_FAILURE", "origin": "pre-implementation sentinel"}
        core.write(self.directory / "baseline.json", baseline)
        result = {"id": "test-strength", "status": "PASS"}
        with (
            patch.object(core, "doctor", return_value={"status": "PASS", "runtime": {}}),
            patch.object(core, "pytest_check", return_value={"id": "acceptance", "status": "PASS"}),
            patch.object(core, "run_check", return_value={"id": "lint", "status": "PASS"}),
            patch.object(core, "replay_regression", return_value=result),
        ):
            core.verify(self.repo, "task", "full", "candidate")
        self.assertEqual(core.load(self.directory / "baseline.json"), baseline)
        self.assertIn("replay", core.load(self.directory / "replay.json")["origin"])

    def test_report_shows_policy_counts_and_exact_wording(self):
        (self.repo / self.source).write_text(
            'class Scheduler:\n    """Public scheduler."""\n    def step(self):\n        # Explain validation\n        raise ValueError("No steps")\n'
        )
        render(self.repo, "task")
        report = (self.directory / "review.md").read_text()
        pr = (self.directory / "PR-DRAFT.md").read_text()
        self.assertIn("Required full checks: 5; executed in candidate: 0", report)
        self.assertIn("Only fork CI enforces policy integrity.", report)
        self.assertIn("Pre-implementation baseline: NOT_RUN", report)
        self.assertIn("No steps", pr)
        self.assertIn("Public scheduler.", pr)
        self.assertIn("# Explain validation", pr)
        self.assertIn("Proposed commit message", pr)
        self.assertIn("Approval: NOT_RUN", pr)
        self.assertIn("No steps", (self.directory / "review.html").read_text())


if __name__ == "__main__":
    unittest.main()
