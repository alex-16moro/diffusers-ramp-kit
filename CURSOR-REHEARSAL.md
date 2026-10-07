# Cursor rehearsal records

## Exploratory rehearsal — setup deviations

Source: user-supplied Cursor summary, not an independently inspected transcript or run archive.
Status: REPORTED LOCAL SUCCESS; clean acceptance NOT established.

The agent challenged a fallback-to-default proposal, created a pinned checkout from a newer fork workspace containing overlays, used a virtualenv workaround, and reported an IndexError baseline, 78 passing scheduler tests, full local verification and a shared handoff. Automatic rule discovery, original workspace mutations, exact elapsed time and intermediate failures were not established by the supplied summary. Preserve the original transcript and logs when available; do not reconstruct missing evidence.

## Clean acceptance run

Status: NOT_RUN. Complete from a fresh Cursor session on the reviewed evaluation installation agreed in alex-16moro/diffusers-ramp-kit#4. Do not use `ramp-base`: since 24 September 2026 it contains a merged fixture solution (see "Fork CI evidence"). The session must run on an engineer host or cloud environment that has never contained the kit repository or completed solutions.

- Cursor version, model, OS and execution environment:
- Absolute folder open in Cursor (clone of the agreed evaluation installation):
- Fork remote URL, reviewed installation SHA, branch and HEAD before creating the contribution branch:
- Fresh engineer-host provisioning record; kit/fixtures/history never present:
- Parent folder `ls -la ..`, host `contribution.patch` search and scan-error review:
- Kit digest and installation/source revision:
- Before-start `git status --short` and `git stash list` output:
- Screenshot of Rules panel showing `ramp-entry.mdc` as Always Apply:
- Only prepared checkout in context; no prior task records or solution:
- Web/MCP/external retrieval disabled:
- Exact request: the fresh task agreed in alex-16moro/diffusers-ramp-kit#4. The empty-list `[999]` request is retired for clean acceptance because the installed kit contains its worked example (`examples/empty-timesteps.json`, the recipe example and scheduler-rule wording).
- Recipe selected, eligibility rationale, related files and any scope expansion:
- Source file/line/symbol citations and pushback:
- Agent-written spec from request/source (not a copied example), and generated scaffold preserving existing tests:
- Pre-implementation regression and separately recorded replay:
- Implementation and copied-method propagation:
- All `.ramp/*/runs/*/result.json` files and associated logs:
- Any genuine failure, diagnosis and repair (NONE if none happened):
- Full verification and shared handoff:
- Exact reviewer-visible wording presented for approval:
- Elapsed time and manual interventions:
- Remaining issues:

Success requires observed automatic discovery, source-grounded design, before/after regression evidence, full current verification and a shared handoff. The operator must record this in Cursor; a CLI replay is not a Cursor acceptance run.

## Separate demonstrations

Record the fallback-to-default variant as a labelled generalisation run. After the clean run, announce and demonstrate a DDPM-only partial fix in a separate disposable checkout; preserve the failed check and repair evidence. Never insert a staged mistake into the clean acceptance record.

## Fork CI evidence

Installation published: `alex-16moro/diffusers` branch `ramp-base` at `961cf0f63de7995bf0d72f99f2517afb4ed40ed2`, one commit on upstream pin `0121a91f9d419ff7234c8a5923f82c244e6f1914`. It carries kit digest `f3e7d284016b7946c8b5f48d2b7f019110efafca682ef578863f28644adbba8d` (kit revision `151e8b3`), created with `onboard`. A fresh `git clone --single-branch --branch ramp-base` tracked all 21 manifest paths and `doctor` returned PASS. No task records, completed contributions or earlier overlay files are on that branch. Branch protection and the required status check are repository settings and are not yet recorded as configured.

Fork CI wiring check (known fixture, not Cursor): draft PR https://github.com/alex-16moro/diffusers/pull/23 (head `eee89448`, base `ramp-base` `961cf0f6`). `Ramp Kit contribution checks / verify` run 35913164061 PASSED: 12/12 checks, 78 scheduler tests, replay failed with the intended `IndexError`, report `READY_FOR_HUMAN_REVIEW`, runtime `torch 2.7.1+cpu` / Python 3.12.14, kit `f3e7d28`. CI patch digest `5380733056ba1589e9cfebe911013967d661c8c25102c4443833847587462995` equals the local digest. This shows the fork CI works end to end; it does not replace a Cursor-authored contribution PR. Do not merge the fixture PR into `ramp-base`.

**Correction (3 October 2026).** The fixture PR #23 was merged into `ramp-base` on 24 September 2026, so `ramp-base` (now `9c3a9d1`) contains the empty-list fixture solution. It is preserved unchanged for history and must not be used as an engineer starting point. The paragraph above describes `ramp-base` as it was at `961cf0f`, before that merge.

`ramp-demo` was then created from the clean installation commit `961cf0f`. It became the fork's default branch, and the coached run below used it as its PR base. At `39c52af` it adds `.cursor/environment.json` and `.cursor/ramp-cloud-setup.sh` and two matching entries in `.ramp-kit/attachment.json`. These were written by hand for Cursor cloud agents: they are not output of kit `f3e7d28`, and `.gitignore` has no exception for them (they were force-added). Its history is upstream pin `0121a91`, then `961cf0f`, then `39c52af`. Neither added commit changes `src/`, `tests/` or `.ramp/`. A scan of every fork branch on 3 October 2026 found that only `ramp-base` and `ramp/empty-timesteps-demo` change the DDPM target files, both with the empty-list fix.

A Cursor-authored PR has since run through fork CI (alex-16moro/diffusers#25, below), but as a coached and assisted run. Still pending for clean acceptance: a PR from the clean run, its Actions URL and conclusion, the base, head and tested-checkout SHAs, and a local patch digest matching the CI digest for the identical submitted patch. It does not have to match a differently worded packaged fixture. Kit-repository CI and local simulations do not satisfy this gate. The current fork workflow records the pin, kit digest and patch digest, but not the PR head SHA, the tested merge SHA, the policy SHA or the run ID (alex-16moro/diffusers-ramp-kit#4, F5).

## Coached and assisted Cursor run: alex-16moro/diffusers#25 (24 September 2026)

Classification: **COACHED AND ASSISTED REHEARSAL. Not clean acceptance.** The useful evidence stands; the run does not establish autonomous discovery or unassisted completion.

- **Environment:** a Cursor cloud agent on `alex-16moro/diffusers` branch `ramp-demo` at `39c52af`. Cursor reported build `bld-20260924-38173dbe-6e4e-4f8d-aad5-648813b016d8`, with `python3.12-venv` added to the base image and the prepared `.ramp-venv` captured in its snapshot. These were reported by Cursor's setup agent and not independently inspected.
- **Request:** the empty-list `[999]` request. The kit's worked example covers this exact task, so the judgment it showed was primed.
- **Coaching:** the prompt, written by the evaluator, prescribed the steps in order: preflight checks, `doctor`, reading the rules and recipe, assessment, spec and `prepare`, baseline, implementation, copy propagation, fast and full verification, and report.
- **Interventions before the measured attempt:** two preflight stops that the prompt required (an untracked legacy `ramp-kit/` folder from a cached environment, then a missing `python3.12-venv`), resolved by recreating the environment and changing its image. The evaluator also added rules on the publication target after an earlier attempt prepared a PR against upstream; that attempt is reported by the user and not otherwise recorded.
- **Interventions during publication:** the evaluator replaced the generated PR body before approving publication. After fork CI rejected the first push (run 35981360248, `verify` job 107573769471: "No task record committed"), the evaluator instructed a second commit adding `.ramp/empty-timesteps/{task,architecture,architecture-history}.json`. The rule and recipe did not tell the agent to commit these.
- **Observed agent work:**
  - REVISE, then COMPATIBLE assessment. The recorded `architecture.json` sources are `scheduling_ddpm.py`, `scheduling_ddpm_parallel.py` and `.ai/references/code_style.md`. The agent's written explanation also cited `docs/source/en/conceptual/philosophy.md`.
  - Baseline `EXPECTED_FAILURE` with `IndexError` at `scheduling_ddpm.py:303`.
  - `ValueError("`timesteps` cannot be empty.")`, copied to `DDPMParallelScheduler` with `utils/check_copies.py --fix_and_overwrite`. The first attempt failed because `ruff` was not on PATH outside the runner; the agent rerun it with `.ramp-venv/bin` on PATH.
  - The parallel test was placed in `tests/schedulers/test_scheduler_ddpm.py` because the parallel test file is not editable.
  - The `# Copied from` marker was located with a workspace search, because `context --symbol` starts at `def`.
- **Local result:** full verification PASS, 12/12 checks, report `READY_FOR_HUMAN_REVIEW`, patch digest `02c34f9999a89c1131050dd001c3e7a0bf1dbb7b4f18db93b0b4bf62108ad3da`.
- **Fork CI:** PR head `e42a269ce5ed5b59b5e6b178d9aa40443133bba2` (commits `7bdce2a` and `e42a269`), base `ramp-demo` `39c52af18ed16405697d66b057ccf238b6c44dde`. Run 35981794009, `verify` job 107575169251: PASS, 12/12 checks, 78 scheduler tests, replay failed with the intended `IndexError`, report `READY_FOR_HUMAN_REVIEW`. The job log shows `patch_sha256` `02c34f99…ad3da`, equal to the local digest, `kit_sha256` `f3e7d284…`, and pin `base_sha` `0121a91f…`. The log does not record which checkout SHAs were tested.
- **Not preserved:** the transcript exists only behind a private Cursor agent link and is not archived here. Start, baseline, first-green and report timings were not recorded.
- **Disposition:** the PR stays open and unmerged as evidence. Its branch contains the empty-list solution and must never be part of an evaluation installation.
