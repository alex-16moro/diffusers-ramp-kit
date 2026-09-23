#!/usr/bin/env python3
"""Publish newly executed CLI evidence and regenerate the distribution manifest."""

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path, help="Output of scripts/reproduce.py")
    args = parser.parse_args()
    evidence = args.run.resolve()
    summary = core.load(evidence / "summary.json")
    if summary["status"] != "PASS" or summary["kit_sha256"] != core.kit_hash():
        raise RuntimeError("Evidence is unsuccessful or belongs to another kit version; rerun reproduce.py")
    checks = KIT / "review-checks"
    # Retain the original historical records byte-for-byte, labelled as superseded.
    archive = KIT / "historical/initial-cli-run"
    if not archive.exists():
        archive.mkdir(parents=True)
        shutil.move(str(KIT / "deliverables"), archive / "deliverables")
        shutil.move(str(checks), archive / "review-checks")
        shutil.move(str(KIT / "review-boundaries.json"), archive / "review-boundaries.json")
        (archive / "README.md").write_text(
            "Historical evidence from the initial recovered environment. Superseded by the current deliverables and review-checks. These original files are preserved unchanged and do not establish current readiness.\n"
        )
    checks.mkdir(exist_ok=True)
    for name, command in (
        ("kit-tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("kit-lint", [sys.executable, "-m", "ruff", "check", "rampkit", "tests", "scripts"]),
        ("kit-format", [sys.executable, "-m", "ruff", "format", "--check", "rampkit", "tests", "scripts"]),
    ):
        result = subprocess.run(command, cwd=KIT, capture_output=True, text=True)
        (checks / f"{name}.log").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f"{name} failed: see review-checks/{name}.log")
    for source, target in [
        (evidence / "local", KIT / "deliverables/empty-timesteps"),
        (evidence / "simulated-ci", KIT / "deliverables/simulated-ci"),
    ]:
        if target.exists():
            shutil.rmtree(target)  # Only generated output directories owned by this exporter.
        shutil.copytree(source, target)
    for path in evidence.iterdir():
        if path.is_file():
            shutil.copyfile(path, checks / path.name)
    core.write(
        checks / "final-integrity.json",
        {
            "kit_sha256": core.kit_hash(),
            "kit_unit_tests": "PASS",
            "kit_lint": "PASS",
            "kit_format": "PASS",
            "normal_commit_fresh_clone_doctor": summary["normal_commit_clone_doctor"],
            "cold_bootstrap": summary["cold_bootstrap"],
            "local_full_checks": summary["local_checks"],
            "simulated_ci_full_checks": summary["simulated_ci_checks"],
            "local_patch_sha256": summary["local_patch_sha256"],
            "simulated_ci_patch_sha256": summary["simulated_ci_patch_sha256"],
            "patch_digests_match": summary["patch_digests_match"],
            "CI_yaml_and_shared_entry_point": "LOCAL_SIMULATION_PASS; remote fork CI NOT_RUN",
            "clean_cursor_acceptance": "NOT_RUN",
            "remote_fork_ci": "NOT_RUN",
            "whole_agent_isolation": "UNMET",
            "provenance": "scripts/reproduce.py from a new documented bootstrap; scripts/export_evidence.py reran kit tests and lint",
        },
    )
    excluded = {"__pycache__", ".ruff_cache", ".pytest_cache", ".git", ".venv"}
    files = [
        p
        for p in KIT.rglob("*")
        if p.is_file()
        and p.name != "CONTENTS.sha256"
        and not excluded.intersection(p.relative_to(KIT).parts)
        and p.suffix != ".pyc"
    ]
    (KIT / "CONTENTS.sha256").write_text(
        "".join(
            f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(KIT).as_posix()}\n"
            for p in sorted(files)
        )
    )
    print(json.dumps({"status": "EXPORTED", "files_in_manifest": len(files), "kit_sha256": core.kit_hash()}))


if __name__ == "__main__":
    main()
