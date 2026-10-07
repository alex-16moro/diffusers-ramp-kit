# Diffusers Contribution Ramp Kit

An agent-facing, repository-installed workflow for a first reviewable Diffusers contribution. The agent selects a recipe for a bounded contribution type, checks architectural fit, and gathers evidence for human review. The first recipe covers input validation in DDPM `set_timesteps` at pinned commit `0121a91f9d419ff7234c8a5923f82c244e6f1914`; rejecting an empty custom timestep list is its worked example. The kit supplies scoped context, a task record, design assessment, a regression scaffold, local checks, and a shared PM/QA/DevOps handoff. Cursor remains the coding agent.

**Start with [START_HERE.md](START_HERE.md).** It contains the exact clean-checkout setup and the single request to give Cursor. See [FINAL-REVIEW.md](FINAL-REVIEW.md) for the requirement scorecard.

## Repository layout

Run commands from this repository root. `run.py` is the entry point; `rampkit/` contains the Python implementation; `profiles/`, `recipes/`, `cursor/`, `runtime/` and `templates/` contain installed resources. `tests/` and `scripts/` hold verification and evidence tooling. `deliverables/` and `review-checks/` contain generated evidence; `historical/` preserves superseded records.

## Recipes organise the journey

Read the [recipe index](recipes/README.md) for supported coverage and selection rules. A recipe supplies relevant context, canonical patterns, related-file obligations, verification and an escape condition when scope grows. Each task supplies its own outcome, criteria and evidence. The engineer describes the problem; Cursor handles selection, task records and commands.

One implemented recipe is sufficient for this version. Other contribution types remain unsupported until their executable path is reviewed and demonstrated. The current profile is deliberately narrower than all scheduler work.

## One engineer starting point

The platform owner prepares and publishes a reviewed installation on `ramp-demo` on the user-owned Diffusers fork, using `onboard`/`attach` on a separate host as described in [RELEASE.md](RELEASE.md). The engineer follows [START_HERE.md](START_HERE.md): clone only that fork branch, bootstrap `.ramp-venv`, run `doctor`, and open the clone in a fresh Cursor session. The same branch supplies onboarding, rule discovery and trusted fork CI policy.

The engineer host must never contain this kit repository or its completed fixtures, `deliverables/` or `historical/` records. A neighbouring folder is still accessible to an agent; workspace instructions alone are insufficient. Keep the source history required for the pinned upstream baseline, but do not fetch contribution branches or solution-bearing history. Record the installation SHA and host/workspace preflight before acceptance.

The attachment appends narrowly scoped `.gitignore` exceptions so plain `git add -A` includes the rules. It adds `.ramp-kit/`, two Cursor rules, Cursor cloud setup (`.cursor/environment.json`, which runs `.cursor/ramp-cloud-setup.sh` to bootstrap `.ramp-venv` and run `doctor`), `.cursorignore` and an additive fork CI workflow, preserving upstream instructions and workflows. Its context, scope and integrity checks are not whole-agent filesystem/network isolation.

## Workflow and reset

The agent reads upstream instructions and the recipe index, selects a matching recipe, checks its boundaries, inspects approved context, and records its architectural assessment with `assess`. If the task exceeds coverage, it proposes a smaller contribution or a reviewed extension before coding.

For the labelled empty-timesteps walkthrough: The proposed `[999]` fallback conflicts with the user's requested behaviour; an empty list should raise a clear `ValueError` in the owning scheduler API. A `REVISE` assessment can record that pushback before a `COMPATIBLE` assessment records the selected plan. The agent writes a new spec under `.ramp/specs/` from the request, using the example only as a schema guide. The agent runs `prepare --spec .ramp/specs/empty-timesteps.json`, adds the three meaningful tests in the existing DDPM test class, and runs `verify empty-timesteps --phase baseline` before editing implementation. The intended failure is an `IndexError` from the original source. It then applies the small guard and uses upstream `utils/check_copies.py --fix_and_overwrite` to refresh the marked parallel copy. `verify empty-timesteps --level full` calls the pinned tests and upstream quality checks; `report empty-timesteps` writes the shared review page, Markdown, PR draft and patch under `.ramp/empty-timesteps/`.

For a fresh rehearsal, make another clone of the reviewed `ramp-demo` branch on a clean engineer host. Do not reset or clean a checkout containing someone's work. Completed contributions and kit verification fixtures stay on the separate owner/reviewer host; do not make them available to the new Cursor session.

To extend this to another input-validation task, choose the owning API and its tests, update the profile's approved references and edit paths, then create a task spec with concrete criteria and mapped test IDs. Run `doctor`, reproduce the regression on original implementation and verify the changed behaviour. New semantics or a different component may require new recipe code and tests; changing profile data alone does not establish support.

## Reading the result

`READY_FOR_HUMAN_REVIEW` means the pinned local full checks passed and the intended regression was observed against the original implementation (pre-implementation baseline and later replay are separately labelled). It is not remote CI, maintainer approval, package publication or deployment. PM validates the outcome and criteria; QA inspects baseline and candidate tests; DevOps checks the fork CI run and release process. A changed source, task, assessment, policy or environment makes prior candidate evidence stale. Human review remains required for the patch and all proposed PR wording.

The business hypothesis is shorter time to the first useful patch and fewer reviewer correction cycles. For a pilot, record elapsed time from first request to passing candidate, reviewer correction count, and first-pass acceptance rate against a comparable baseline. This one local rehearsal is technical evidence, not a measured business improvement.

The empty-timesteps walkthrough is a worked demonstration, not an unseen-task acceptance test. See `ACCEPTANCE.md` on the evaluator host for the separate acceptance protocol.

See `DEMO.md` for the 8–12 minute interview journey and `DECISIONS.md` for design trade-offs and limitations.

See `RELEASE.md` for the two-stage fork CI setup and executable optional packaging commands; `MAINTENANCE.md` for profile updates and a second-task extension example; `CURSOR-REHEARSAL.md` for the remaining runtime acceptance check.
