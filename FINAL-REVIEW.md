# Final review against the agreed build

**Verdict: changes implemented; CLI evidence is regenerated from the documented bootstrap. The agreed MVP remains PARTIAL until a clean Cursor acceptance run and a real Diffusers fork CI run are recorded.**

The current measured results are in `review-checks/final-integrity.json`, `review-checks/summary.json` and their logs. `scripts/reproduce.py` performs a labelled CLI fixture rehearsal and a local base-policy CI simulation. It does not represent an autonomous Cursor run. `scripts/export_evidence.py` reruns kit checks, copies newly executed evidence and generates the manifest. Historical recovered-environment evidence is preserved unchanged under `historical/initial-cli-run/` and is not current proof.

## Requirement scorecard

| Requirement | Implemented evidence | Status and remaining limit |
|---|---|---|
| 1. First correct contribution | Commit-safe attachment, explicit Python 3.12 bootstrap, agent-written spec instructions and task-derived scaffold; fresh-clone doctor and CLI regression journey | PARTIAL: clean Cursor rerun pending; exploratory run recorded with setup deviations. Automatic discovery and agent spec authorship remain unverified in the clean session. |
| 2. Catch mistakes and strengthen tests | Mapped assertion check with negative fixture, actionable baseline failures, correct check/error exit codes, separate pre-implementation and replay records, full affected-module verification | PASS for the scoped local MVP when the generated checks pass. Non-constant assertion presence is not proof of semantic quality or reachability. Pre-implementation order is instructed; replay can independently support readiness, with truthful labels. |
| 3. CI, guardrails and delivery path | Installation survives normal commit/clone; base-policy runner simulation verifies the same patch; repository-root kit CI workflow; policy digests and check counts displayed | PARTIAL until actual Diffusers fork PR CI runs against `ramp-base`. Kit repository Actions and local simulations do not satisfy that gate. Whole-agent filesystem/network isolation remains UNMET. Optional packaging and deployment NOT_RUN. |
| 4. Maintainability | Task validation and mapped scaffold generation, pinned source hashes/symbols, regression tests and maintenance instructions | PARTIAL: bounded recipe mechanics are tested, but the second-task prepare/baseline/full-verify path remains NOT_RUN. Other scheduler families are not demonstrated. |
| 5. Shared PM/QA/DevOps handoff | Stable patch digest, separate baseline/replay, required/executed counts, installation/runner policy digest, draft wording inventory and precise delivery status | PASS for generated local handoff evidence. Exact wording approval, remote fork CI and collaborative human sign-off remain NOT_RUN. |

## Review requests addressed

- **A1:** `requirements.txt` and narrowly scoped `.gitignore` exceptions; unit and integration checks stage with plain `git add -A`, commit, clone, and verify every attachment manifest path.
- **A2:** all bootstrap selection uses `${PYTHON:-python3.12}`; missing interpreter/venv diagnostics include explicit recovery. A partial environment without pip is recreated on retry. Cold installation evidence is generated. Interpreter-selection failure paths are additionally tested with simulated executables; the actual host's `python3` is also 3.12, so the cold run is not a test on a real 3.11-default machine.
- **A3:** a shared deterministic patch function uses full blob IDs and explicit formatting. Local/simulation digests are compared. Deliverables come from the documented cold bootstrap; old evidence is separately archived.
- **A4:** missing kit ignore/workflow files restored; the active repository-root workflow runs directly against the root-level kit. No prepared task snapshot is claimed or shipped; its obsolete manifest entries are removed by regeneration.
- **A5:** the entry rule reads `.ai/AGENTS.md`, uses `.ramp-venv`, and prohibits redundant setup or networked skill installation/listing during this prepared session. Upstream coding and human-review guidance remain applicable.
- **B1:** mapped methods without a supported assertion fail before execution. `pass`, raise-only stubs and assertions hidden in nested helpers are negative cases. No mutation-testing or universal quality claim.
- **B2:** baseline pass, skip, wrong exception/origin and execution error produce distinct reasons. Missing/pending design assessment is a check failure (exit 1).
- **B3:** baseline and replay have independent records and provenance. Replay never overwrites or fabricates the pre-implementation record.
- **B4:** handoff displays required/executed counts and runner/installation digests. The installation reference is explicitly locally editable. Only fork CI enforces policy integrity, subject to maintainer protection of its base policy and workflow.
- **B5:** the agent must author a spec from the request and inspected code; the example is schema guidance. `prepare` validates it and creates method stubs from mapped IDs. Actual autonomous authorship remains part of the pending Cursor acceptance run.
- **B6:** generated reports and PR drafts include proposed commit wording, new/changed Python literals, docstrings and comments, with approval NOT_RUN. Review the complete patch too; dynamic text cannot be exhaustively classified by a small static extractor.

## Independent re-review corrections (C1–C4, D1–D5)

- **C1/C2:** one documented engineer path: clone the reviewed fork's `ramp-base`. Owner-only `onboard`/`attach` prepares that branch on a separate host. The engineer host must never contain this kit repo, solution fixtures or prior evidence; record the host scan, parent listing, remote, branch and installation SHA. This is an operator precondition, not whole-agent isolation. Actual clean-host acceptance remains NOT_RUN.
- **C3:** scaffold generation parses mapped test files, marks existing methods as evidence to preserve, and generates stubs only for missing methods. The CLI reproduction checks the real upstream AC3 method is never stubbed.
- **C4:** the scheduler rule correctly describes existing `assertRaises(ValueError, msg=...)` and distinguishes `assertRaisesRegex` for new message assertions.
- **D1:** literal-only assertions are rejected, including `assertTrue(True)`, constant comparisons and dynamic failure-message variants. A labelled negative fixture and candidate-gate tests cover these cases. This remains a small syntactic safeguard, not semantic test-quality proof.
- **D2:** Requirement 4 is PARTIAL until the second-task CLI journey actually runs; the plan in MAINTENANCE.md is explicitly NOT_RUN.
- **D3:** generated provenance uses “Installation digest” and `installation_kit_sha256`, explicitly sourced from the locally editable attachment manifest, not a signed release.
- **D4:** onboarding clone/OS failures explain the creation problem and suggest a new writable destination under the current workspace. The operator chooses it; no automatic relocation occurs.
- **D5:** the installed recipe points to `.ramp-kit/examples/empty-timesteps.json` as schema guidance.

Opus's supplied independent re-review of `a92e3b5` reports Python 3.12 selection on a host whose `python3` is 3.11, a fresh 12-check CLI journey and green main kit CI. That is separately attributed review evidence, not a rerun by this builder or a clean Cursor/fork PR acceptance record. The current generated results linked above come from rerunning the changed kit.

## Remaining acceptance evidence

1. Perform the exact `[999]` clean Cursor run from a clone of the reviewed fork `ramp-base` on a host without the kit repository, using `START_HERE.md` and record it in `CURSOR-REHEARSAL.md`, including workspace/rule screenshot, initial Git status/stashes, model/version, timings/interventions and every result/log.
2. Keep the exploratory fallback variant separate. Demonstrate the announced DDPM-only staged failure after the clean run in another disposable checkout.
3. `ramp-base` is published on the user-owned Diffusers fork at `961cf0f` (kit `f3e7d28`; see CURSOR-REHEARSAL.md). Next, run a real contribution PR against it. Record its Actions URL/conclusion, base/head SHAs and patch digest matching the local contribution. Publishing this kit PR does not imply that the separate fork was modified or verified.
4. Packaged evidence under `deliverables/` and `review-checks/` was generated with kit `f3e7d28`. The `WRONG_BASE`/`ATTACH_CONFLICT` message change moves the kit digest to `71a070b`; regenerate evidence with `scripts/reproduce.py` and `scripts/export_evidence.py` before merging it, and upgrade `ramp-base` only as an explicit, reviewed kit upgrade.

No container isolation, extra agents, MCP, database, hooks, expanded scheduler recipe or packaging automation was added. Business improvement remains a measurement hypothesis, not an observed time-saving claim.
