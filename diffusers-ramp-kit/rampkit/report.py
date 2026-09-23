from __future__ import annotations

import html
from pathlib import Path

from .core import digest, fingerprint, git, load, read_task, readiness, task_dir, write


def render(repo: Path, task_id: str) -> dict:
    task = read_task(repo, task_id)
    directory = task_dir(repo, task_id)
    state = readiness(repo, task)
    candidate = state["candidate"] or {}
    baseline = state["baseline"] or {}
    assessment = load(directory / "architecture.json")
    stale = state["status"] == "STALE"
    checks = candidate.get("checks", [])
    acceptance = next((c for c in checks if c["id"] == "acceptance"), {})
    results = {(t["class"], t["name"]): t["status"] for t in acceptance.get("tests", [])}
    rows = []
    for criterion in task["criteria"]:
        statuses = []
        for node in criterion["tests"]:
            path, klass, name = node.split("::")
            key = (path.removesuffix(".py").replace("/", ".") + "." + klass, name)
            statuses.append(results.get(key, "NOT_RUN"))
        status = "PASS" if statuses and set(statuses) == {"PASS"} else ", ".join(sorted(set(statuses)))
        rows.append((criterion["id"], criterion["text"], "STALE" if stale else status, criterion["tests"]))
    baseline_status = "STALE" if stale else baseline.get("status", "NOT_RUN")
    strength = next((c for c in checks if c["id"] == "test-strength"), {})
    strength_status = "STALE" if stale else strength.get("status", "NOT_RUN")
    patch = git(repo, "diff", "--binary", task["base_sha"], "--", *task["editable_files"])
    patch_paths = (
        git(repo, "diff", "--name-only", task["base_sha"], "--", *task["editable_files"])
        .decode()
        .splitlines()
    )
    md = [
        f"# {task['title']}",
        "",
        f"**{state['status']}** — {state['reason']}",
        "",
        "## PM — requested outcome",
        task["request"],
        "",
        "| Criterion | Expected behaviour | Evidence status |",
        "|---|---|---|",
    ]
    md += [f"| {i} | {text.replace('|', '/')} | {status} |" for i, text, status, _ in rows]
    md += [
        "",
        "Exclusions: " + "; ".join(task.get("exclusions", [])),
        "",
        "Next action: confirm these criteria reflect the requested outcome. No business approval is recorded.",
        "",
        "## Engineering — design and review",
        f"Assessment: {assessment['decision']} (agent judgement).",
        assessment.get("rationale", ""),
        "Changed paths: " + ", ".join(patch_paths),
        "",
        "Source references:",
    ]
    md += [f"- `{p}`" for p in assessment.get("sources", [])]
    md += [
        "",
        "Review questions: Is the error contract appropriate? Do valid inputs and argument-error precedence remain unchanged?",
        "",
        "## QA — criteria and tests",
    ]
    md += [f"- {i}: " + ", ".join(f"`{t}`" for t in tests) for i, _, _, tests in rows]
    md += [
        "",
        f"Original implementation: {baseline_status}.",
        f"Fix-removal replay: {strength_status}.",
        "The replay runs current tests against the pinned original implementation in a disposable snapshot. A PASS means the intended regression failed again.",
        "",
        "| Check | Status | Duration | Log |",
        "|---|---|---|---|",
    ]
    for check in checks:
        status = "STALE" if stale else check["status"]
        relative = Path(check["log"]).relative_to(directory.relative_to(repo)).as_posix()
        md.append(f"| {check['id']} | {status} | {check['seconds']}s | [{check['id']} log]({relative}) |")
    md += [f"- {f['rule']}: {f['message']}" for f in candidate.get("findings", [])]
    md += [
        "",
        "Not covered: arbitrary scheduler types, GPU execution, all input shapes and diffusion numerical correctness.",
        "QA next action: inspect the failing baseline and passing candidate logs; replay any disputed criterion.",
        "",
        "## DevOps — delivery handoff",
        f"- Upstream base: `{task['base_sha']}`",
        f"- Kit content digest: `{candidate.get('kit_sha256', 'NOT_RUN')}`",
        f"- Current patch digest: `{digest(patch)}`",
        f"- Environment: `{candidate.get('runtime', {})}`",
        "- Remote CI: NOT_RUN. Additive workflow configured; inspect the actual fork PR job before promotion.",
        "- Package build / isolated consumer smoke test: NOT_RUN (optional feature omitted).",
        "- Human review / production deployment: NOT_RUN.",
        f"- Shared runner: `python .ramp-kit/run.py --repo . verify {task_id} --level full`",
        "- Promotion: maintainer-approved fork CI, human review, then the team’s package/release procedure. See RELEASE.md in the kit bundle for executable build and smoke instructions.",
        "- Rollback: redeploy the prior approved wheel and restore its dependency lock; verify the consumer health checks.",
        "",
        "## Boundaries and limitations",
        "- Context/path and patch-scope checks are enforced by the kit. Whole-agent filesystem and network isolation are UNMET.",
        "- An external Cursor tool can access beyond these helpers unless an operator provides separate isolation. Disable external retrieval for the rehearsal.",
        "- Fresh Cursor rule discovery and autonomous completion remain UNVERIFIED until the operator records a fresh-session rehearsal.",
        "- Reports are snapshots. Run report again after edits; copied HTML cannot detect later filesystem changes.",
        "- No human approvals are fabricated. Review all PR wording before publishing.",
    ]
    markdown = "\n".join(md) + "\n"
    (directory / "review.md").write_text(markdown)

    def esc(value):
        return html.escape(str(value), quote=True)

    criteria_html = "".join(
        f'<tr><th scope="row">{esc(i)}</th><td>{esc(t)}</td><td>{esc(s)}</td></tr>' for i, t, s, _ in rows
    )
    check_html = []
    for c in checks:
        relative = Path(c["log"]).relative_to(directory.relative_to(repo)).as_posix()
        status = "STALE" if stale else c["status"]
        counts = c.get("counts", {})
        check_html.append(
            f'<tr><th scope="row">{esc(c["id"])}</th><td>{esc(status)}</td><td>{esc(c["seconds"])}s</td><td><a href="{esc(relative)}">Log</a></td></tr>'
        )
        check_html.append(
            f'<tr><td colspan="4"><details><summary>Command and evidence</summary><pre>{esc(c["command"])}</pre><p>Exit code: {esc(c["exit_code"])}; test counts: {esc(counts)}</p></details></td></tr>'
        )
    mapping = "".join(
        f"<li><strong>{esc(i)}</strong><ul>"
        + "".join(f"<li><code>{esc(t)}</code></li>" for t in tests)
        + "</ul></li>"
        for i, _, _, tests in rows
    )
    other_sections = []
    for section in (
        "Engineering — design and review",
        "DevOps — delivery handoff",
        "Boundaries and limitations",
    ):
        start = md.index("## " + section) + 1
        end = next((n for n in range(start, len(md)) if md[n].startswith("## ")), len(md))
        other_sections.append(
            "<section><h2>"
            + esc(section)
            + "</h2>"
            + "".join("<p>" + esc(line) + "</p>" for line in md[start:end] if line)
            + "</section>"
        )
    document = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ramp Kit — Shared change review</title><style>
body{margin:0;background:#f1f4f8;color:#18283c;font:16px/1.55 system-ui,sans-serif}main{max-width:1050px;margin:32px auto;padding:32px;background:white;border-top:6px solid #3158c8;border-radius:8px}h1{line-height:1.2}h2{margin-top:30px}table{border-collapse:collapse;width:100%;margin:16px 0}th,td{text-align:left;padding:12px;border-bottom:1px solid #d6deea;vertical-align:top}thead{background:#edf2fa}code,pre{font-family:ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}p{overflow-wrap:anywhere}a{color:#1745a4}summary{cursor:pointer}.status{padding:16px;background:#edf2fa;font-weight:650}section{border-top:1px solid #d6deea;margin-top:24px}@media(max-width:700px){main{margin:8px;padding:16px}th,td{padding:8px;font-size:14px}}</style><main>"""
    document += f'<p>RAMP KIT / SHARED CHANGE RECORD</p><h1>{esc(task["title"])}</h1><p class="status">{esc(state["status"])} — {esc(state["reason"])}</p>'
    document += f"<h2>PM — requested outcome</h2><p>{esc(task['request'])}</p><table><thead><tr><th>Criterion</th><th>Expected behaviour</th><th>Evidence</th></tr></thead><tbody>{criteria_html}</tbody></table><p>PM next action: confirm the criteria. No business sign-off is implied.</p>"
    document += other_sections[0]
    document += f"<section><h2>QA — tests and sensitivity</h2><p>Original implementation: {esc(baseline_status)}. Fix-removal replay: {esc(strength_status)}.</p><p>Replay PASS means the regression failed again after restoring original implementation in a disposable snapshot.</p><details><summary>Acceptance criteria → executed tests</summary><ul>{mapping}</ul></details><table><thead><tr><th>Check</th><th>Status</th><th>Duration</th><th>Evidence</th></tr></thead><tbody>{''.join(check_html)}</tbody></table><p>QA next action: inspect the baseline and candidate logs. GPU behaviour and the full Diffusers suite are outside this check.</p></section>"
    document += "".join(other_sections[1:]) + "</main></html>"
    (directory / "review.html").write_text(document)
    pr = [
        f"# {task['title']}",
        "",
        "## Why",
        task["request"],
        "",
        "## What changed",
        assessment.get("rationale", ""),
        "",
        "## Validation",
        f"{state['status']}: {state['reason']}",
    ]
    pr += [f"- {c['id']}: {'STALE' if stale else c['status']}" for c in checks]
    pr += [
        "",
        "## Reviewer attention",
        "Confirm error wording, input compatibility, and argument-error precedence.",
        "",
        "DRAFT: a human must review and approve this exact wording before publication. Remote CI, human approval and deployment have not been established.",
    ]
    (directory / "PR-DRAFT.md").write_text("\n".join(pr) + "\n")
    (directory / "contribution.patch").write_bytes(patch)
    write(
        directory / "handoff.json",
        {
            "status": state["status"],
            "fingerprint": fingerprint(repo, task),
            "patch_sha256": digest(patch),
            "criteria": rows,
        },
    )
    return {
        "status": state["status"],
        "reason": state["reason"],
        "report": str(directory / "review.html"),
        "markdown": str(directory / "review.md"),
        "pr_draft": str(directory / "PR-DRAFT.md"),
    }
