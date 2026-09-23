#!/usr/bin/env python3
"""CLI integration rehearsal using a labelled known patch, never Cursor evidence.

Creates a disposable checkout; bootstraps the documented environment; tests normal
commit/clone installation and the exact base-policy/candidate runner arrangement.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))
from rampkit import core  # noqa: E402
from rampkit.cli import onboard  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True, help="New disposable directory")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    if work.exists():
        parser.error("--work must not exist")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    commands = []

    def run(argv, cwd, name, expected=0):
        result = subprocess.run([str(a) for a in argv], cwd=cwd, capture_output=True, text=True)
        (output / f"{name}.log").write_text(result.stdout + result.stderr)
        commands.append({"name": name, "command": [str(a) for a in argv], "exit_code": result.returncode})
        core.write(output / "commands.json", commands)
        if result.returncode != expected:
            raise RuntimeError(
                f"{name}: expected exit {expected}, observed {result.returncode}; see {output}"
            )
        return result.stdout

    installed = onboard(args.source.resolve(), work)
    core.write(output / "onboarding.json", installed)
    run(["bash", work / ".ramp-kit/runtime/bootstrap.sh", work], work, "cold-bootstrap")
    python = work / ".ramp-venv/bin/python"

    def cli(name, *args, runner=None, checkout=work, expected=0):
        raw = run(
            [python, runner or work / ".ramp-kit/run.py", "--repo", checkout, *args], work, name, expected
        )
        return json.loads(raw)

    cli("doctor", "doctor")
    run(["git", "add", "-A"], work, "stage-installation")
    run(
        [
            "git",
            "-c",
            "user.name=Ramp Kit verification",
            "-c",
            "user.email=verification@example.invalid",
            "commit",
            "-qm",
            "Install reviewed kit for disposable integration test",
        ],
        work,
        "commit-installation",
    )
    manifest = core.load(work / ".ramp-kit/attachment.json")
    tracked = set(run(["git", "ls-files"], work, "tracked-installation").splitlines())
    missing = sorted(set(manifest["files"]) - tracked)
    if missing:
        raise RuntimeError(f"Manifest files not committed: {missing}")
    base_commit = core.git(work, "rev-parse", "HEAD").decode().strip()
    policy = work.parent / (work.name + "-policy")
    candidate = work.parent / (work.name + "-candidate")
    if policy.exists() or candidate.exists():
        raise RuntimeError("Policy/candidate destination already exists; choose another --work")
    run(
        ["git", "clone", "--no-local", "--single-branch", "--branch", "ramp-base", "--no-tags", work, policy],
        work,
        "clone-installation",
    )
    cli("fresh-clone-doctor", "doctor", runner=policy / ".ramp-kit/run.py", checkout=policy)
    run(["git", "switch", "-c", "ramp/fixture-contribution"], work, "contribution-branch")

    # Deliberately use a known fixture for reproducibility. A clean Cursor session
    # must independently derive its spec and implementation from the user request.
    cli("prepare", "prepare", "--spec", KIT / "examples/empty-timesteps.json")
    scaffold = (work / ".ramp/empty-timesteps/test-scaffold.txt").read_text()
    existing_method = "test_custom_timesteps_passing_both_num_inference_steps_and_timesteps"
    if f"def {existing_method}" in scaffold or f"do not modify: {existing_method}" not in scaffold:
        raise RuntimeError("Scaffold did not preserve the existing upstream mutual-exclusion test")
    cli(
        "assess",
        "assess",
        "empty-timesteps",
        "--decision",
        "COMPATIBLE",
        "--rationale",
        "Reject an explicitly empty custom schedule with a clear error at its owning API; preserve valid input and mutual-exclusion precedence.",
        "--source",
        ".ai/references/code_style.md",
        "--source",
        "docs/source/en/conceptual/philosophy.md",
        "--source",
        "src/diffusers/schedulers/scheduling_ddpm.py",
    )
    patch = KIT / "tests/fixtures/contribution.patch"
    test_file = core.profile()["test_file"]
    run(["git", "apply", "--include=" + test_file, patch], work, "apply-test-fixture")
    cli("baseline", "verify", "empty-timesteps", "--phase", "baseline")
    run(["git", "apply", "--exclude=" + test_file, patch], work, "apply-implementation-fixture")
    local = cli("local-full", "verify", "empty-timesteps", "--level", "full")
    cli("local-report", "report", "empty-timesteps")
    shutil.copytree(work / ".ramp/empty-timesteps", output / "local", dirs_exist_ok=True)

    # Only task and assessment are submitted to the CI simulation, never local green evidence.
    run(
        [
            "git",
            "add",
            *core.profile()["editable_files"],
            ".ramp/empty-timesteps/task.json",
            ".ramp/empty-timesteps/architecture.json",
        ],
        work,
        "stage-candidate",
    )
    run(
        [
            "git",
            "-c",
            "user.name=Ramp Kit verification",
            "-c",
            "user.email=verification@example.invalid",
            "commit",
            "-qm",
            "Apply labelled fixture for disposable CI simulation",
        ],
        work,
        "commit-candidate",
    )
    head_commit = core.git(work, "rev-parse", "HEAD").decode().strip()
    run(["git", "clone", "--no-hardlinks", work, candidate], work, "clone-candidate")
    run(["git", "config", "core.abbrev", "12"], candidate, "different-git-abbreviation")
    if (policy / ".ramp-kit/attachment.json").read_bytes() != (
        candidate / ".ramp-kit/attachment.json"
    ).read_bytes():
        raise RuntimeError("Candidate changed base manifest")
    if (policy / ".github/workflows/ramp-kit.yml").read_bytes() != (
        candidate / ".github/workflows/ramp-kit.yml"
    ).read_bytes():
        raise RuntimeError("Candidate changed workflow")
    run(
        ["git", "diff", "--exit-code", base_commit, "--", "setup.py", "pyproject.toml"],
        candidate,
        "protected-build-inputs",
    )
    # Same pinned environment, source imports selected by runtime_env(candidate).
    # This is explicitly local CI simulation, not a second cold install or remote fork CI.
    simulated = cli(
        "simulated-ci-full",
        "verify",
        "empty-timesteps",
        "--level",
        "full",
        runner=policy / ".ramp-kit/run.py",
        checkout=candidate,
    )
    cli(
        "simulated-ci-report",
        "report",
        "empty-timesteps",
        runner=policy / ".ramp-kit/run.py",
        checkout=candidate,
    )
    shutil.copytree(candidate / ".ramp/empty-timesteps", output / "simulated-ci", dirs_exist_ok=True)
    if local["patch_sha256"] != simulated["patch_sha256"]:
        raise RuntimeError("Local and simulated CI patch digests differ")
    if (candidate / ".ramp/empty-timesteps/baseline.json").exists():
        raise RuntimeError("Replay fabricated a pre-implementation baseline")
    summary = {
        "status": "PASS",
        "kind": "CLI fixture rehearsal and LOCAL CI simulation, not Cursor or remote fork CI",
        "base_commit": base_commit,
        "candidate_commit": head_commit,
        "kit_sha256": manifest["kit_sha256"],
        "normal_commit_clone_doctor": "PASS",
        "cold_bootstrap": "PASS",
        "local_checks": len(local["checks"]),
        "simulated_ci_checks": len(simulated["checks"]),
        "local_patch_sha256": local["patch_sha256"],
        "simulated_ci_patch_sha256": simulated["patch_sha256"],
        "patch_digests_match": True,
        "preimplementation_baseline_preserved": True,
        "fixture_sha256": hashlib.sha256(patch.read_bytes()).hexdigest(),
        "clean_cursor_run": "NOT_RUN",
        "remote_fork_ci": "NOT_RUN",
    }
    core.write(output / "summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
