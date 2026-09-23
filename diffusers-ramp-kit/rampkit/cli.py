from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from . import core
from .report import render


def onboard(source: Path, destination: Path) -> dict:
    """Create a separate pinned checkout with no completed solution or old task evidence."""
    destination = destination.resolve()
    if destination.exists():
        raise core.RampError("Onboarding destination must not exist; choose a new directory.")
    core.git(source, "cat-file", "-e", f"{core.profile()['base_sha']}^{{commit}}")
    result = subprocess.run(
        ["git", "clone", "--no-hardlinks", "--no-checkout", str(source.resolve()), str(destination)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise core.RampError(f"Cannot create onboarding checkout: {result.stderr}")
    core.git(destination, "checkout", "-b", "ramp/first-contribution", core.profile()["base_sha"])
    core.git(destination, "remote", "set-url", "origin", core.profile()["upstream"])
    installed = attach(destination)
    return {
        "status": "ONBOARDING_READY",
        "checkout": str(destination),
        "attachment": installed,
        "next_action": "Bootstrap dependencies, then open ONLY this checkout in a fresh Cursor session. Do not add the kit bundle or completed examples to that workspace.",
    }


def attach(repo: Path) -> dict:
    root = core.kit_root()
    check = core.doctor(repo, dependencies=False)
    if check["status"] != "PASS":
        raise core.RampError("; ".join(check["findings"]))
    dest = core.safe_path(repo, ".ramp-kit")
    if dest.exists():
        old = core.load(dest / "attachment.json")
        if old["kit_sha256"] != core.kit_hash(root):
            raise core.RampError(
                "A different kit is already attached. Review an explicit upgrade; nothing overwritten."
            )
        for relative, checksum in old["files"].items():
            path = core.safe_path(repo, relative)
            if not path.is_file() or core.digest(path.read_bytes()) != checksum:
                raise core.RampError(f"Attached file changed: {relative}; refusing overwrite.")
        return {"status": "ALREADY_ATTACHED", "kit_sha256": old["kit_sha256"]}
    mapping = {}
    for folder in ("rampkit", "profiles", "recipes", "templates", "examples", "runtime", "cursor"):
        for path in sorted((root / folder).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                mapping[f".ramp-kit/{path.relative_to(root).as_posix()}"] = path
    mapping[".ramp-kit/run.py"] = root / "run.py"
    for name in ("ramp-entry.mdc", "ramp-scheduler.mdc"):
        mapping[f".cursor/rules/{name}"] = root / "cursor" / name
    mapping[".github/workflows/ramp-kit.yml"] = root / "templates/fork-ci.yml"
    mapping[".cursorignore"] = root / "templates/cursorignore.txt"
    # All conflict checks happen before writes; existing instruction files are never touched.
    for relative in mapping:
        if core.safe_path(repo, relative).exists():
            raise core.RampError(f"Attachment would overwrite {relative}; choose a clean checkout.")
    for relative, source in mapping.items():
        target = core.safe_path(repo, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    manifest = {
        "kit_sha256": core.kit_hash(root),
        "base_sha": core.profile()["base_sha"],
        "files": {name: core.digest(path.read_bytes()) for name, path in mapping.items()},
    }
    core.write(dest / "attachment.json", manifest)
    return {
        "status": "ATTACHED",
        "kit_sha256": manifest["kit_sha256"],
        "files_added": len(mapping),
        "next_action": "Open this checkout in a fresh Cursor session and describe the task.",
    }


def parser():
    p = argparse.ArgumentParser(description="Agent-facing first-contribution workflow; all results are JSON.")
    p.add_argument("--repo", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("attach")
    sub.add_parser("doctor")
    q = sub.add_parser("onboard")
    q.add_argument("--dest", type=Path, required=True)
    q = sub.add_parser("context")
    q.add_argument("path")
    q.add_argument("--symbol")
    q = sub.add_parser("prepare")
    q.add_argument("--spec", type=Path, required=True)
    q = sub.add_parser("assess")
    q.add_argument("task")
    q.add_argument("--decision", choices=["COMPATIBLE", "REVISE", "NEEDS_MAINTAINER"], required=True)
    q.add_argument("--rationale", required=True)
    q.add_argument("--source", action="append", required=True)
    q.add_argument("--alternative", default="")
    q = sub.add_parser("verify")
    q.add_argument("task")
    q.add_argument("--level", choices=["fast", "full"], default="fast")
    q.add_argument("--phase", choices=["baseline", "candidate"], default="candidate")
    q = sub.add_parser("report")
    q.add_argument("task")
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    repo = args.repo.resolve()
    try:
        if args.command == "attach":
            result = attach(repo)
        elif args.command == "onboard":
            result = onboard(repo, args.dest)
        elif args.command == "doctor":
            result = core.doctor(repo)
        elif args.command == "context":
            result = core.context(repo, args.path, args.symbol)
        elif args.command == "prepare":
            result = core.prepare(repo, args.spec.resolve())
        elif args.command == "assess":
            result = core.assess(
                repo, args.task, args.decision, args.rationale, args.source, args.alternative
            )
        elif args.command == "verify":
            result = core.verify(repo, args.task, args.level, args.phase)
        else:
            result = render(repo, args.task)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        status = result.get("status")
        if status == "ERROR":
            return 2
        return 1 if status in ("FAIL", "INCOMPLETE", "STALE", "NOT_RUN") else 0
    except (core.RampError, OSError, ValueError, KeyError, TypeError) as exc:
        print(
            json.dumps(
                {
                    "status": "ERROR",
                    "message": str(exc),
                    "next_action": "Resolve this configuration or input error; do not claim verification passed.",
                }
            )
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
