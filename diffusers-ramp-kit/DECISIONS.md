# Decision record

| Choice | Evidence | Trade-off / limitation |
|---|---|---|
| Pin upstream and one DDPM validation recipe | The scheduler has an existing custom-input branch and tests; the parallel method is marked as a copy. | Narrow coverage; no claim of a universal contribution agent. |
| Reject the suggested `[999]` fallback | `.ai/references/code_style.md` asks for clear errors rather than silently correcting unsupported input; `set_timesteps` currently indexes the empty list. | Adds a specific error contract, subject to maintainer review. |
| Keep Cursor as the agent, Python as local machinery | Cursor rules guide design, while deterministic commands produce test evidence and a shared handoff. | Rule discovery and compliance in a fresh Cursor session are not yet verified. |
| Reuse upstream copy and quality tooling | The parallel method is tagged `# Copied from`; the existing Makefile and check scripts are the repository's gates. | The profile pins commands; upstream changes require owner review. |
| Check approved context, symlinks and edit scope | `safe_path`, profile sources and the task allowlist constrain kit commands and evidence. | The Cursor agent itself has no enforced OS or network sandbox. |
| Keep approval with humans | The upstream agent guide requires human review of PR-facing text and prohibits autonomous publication. | Local `READY_FOR_HUMAN_REVIEW` does not certify remote CI, package installation or production readiness. |

Historical build observation (not evidence for the current regenerated run): `utils/check_copies.py --fix_and_overwrite` initially could not find the `ruff` executable because the resumed shell lacked the environment's `bin` directory on `PATH`. Rerunning with the pinned environment on `PATH` refreshed the parallel copy; the full gate then passed. A separate broken Python symlink in the recovered environment was repaired locally before testing. These are environment repairs, not Diffusers source changes.

Final review corrections: added disposable original-implementation replay; corrected count-based acceptance to a direct test; tested both scheduler classes; made every displayed check stale when inputs drift; included execution logs; introduced clean onboarding and base-commit CI policy; isolated the upstream dependency-table check because it writes generated data. No separate Grokbot service, MCP server, automatic edit hooks, universal generator or package smoke feature was added, in accordance with the final agreed scope.
