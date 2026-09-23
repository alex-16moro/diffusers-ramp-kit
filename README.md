# Diffusers Contribution Ramp Kit

An agent-facing, repository-installed workflow for a first reviewable Diffusers contribution. Its supported example is rejecting an empty custom timestep list in `DDPMScheduler.set_timesteps` at pinned commit `0121a91f9d419ff7234c8a5923f82c244e6f1914`. The kit supplies scoped context, a task record, design assessment, a regression scaffold, local checks, and a shared PM/QA/DevOps handoff. Cursor remains the coding agent.

**Start with [START_HERE.md](START_HERE.md).** It contains the exact clean-checkout setup and the single request to give Cursor. See [FINAL-REVIEW.md](FINAL-REVIEW.md) for the requirement scorecard.

## Repository layout

Run commands from this repository root. `run.py` is the entry point; `rampkit/` contains the Python implementation; `profiles/`, `recipes/`, `cursor/`, `runtime/` and `templates/` contain installed resources. `tests/` and `scripts/` hold verification and evidence tooling. `deliverables/` and `review-checks/` contain generated evidence; `historical/` preserves superseded records.

## One engineer starting point

The platform owner prepares and publishes the reviewed `ramp-base` branch on the user-owned Diffusers fork, using `onboard`/`attach` on a separate host as described in [RELEASE.md](RELEASE.md). The engineer follows [START_HERE.md](START_HERE.md): clone only that fork branch, bootstrap `.ramp-venv`, run `doctor`, and open the clone in a fresh Cursor session. The same branch supplies onboarding, rule discovery and trusted fork CI policy.

The engineer host must never contain this kit repository or its completed fixtures, `deliverables/` or `historical/` records. A neighbouring folder is still accessible to an agent; workspace instructions alone are insufficient. Keep the source history required for the pinned upstream baseline, but do not fetch contribution branches or solution-bearing history. Record the installation SHA and host/workspace preflight before acceptance.

The attachment appends narrowly scoped `.gitignore` exceptions so plain `git add -A` includes the rules. It adds `.ramp-kit/`, two Cursor rules, `.cursorignore` and an additive fork CI workflow, preserving upstream instructions and workflows. Its context, scope and integrity checks are not whole-agent filesystem/network isolation.

## Workflow and reset

The agent reads upstream instructions, approved context and the recipe, then records its assessment with `assess`. The proposed `[999]` fallback conflicts with the user's requested behaviour; an empty list should raise a clear `ValueError` in the owning scheduler API. A `REVISE` assessment can record that pushback before a `COMPATIBLE` assessment records the selected plan. The agent writes a new spec under `.ramp/specs/` from the request, using the example only as a schema guide. The agent runs `prepare --spec .ramp/specs/empty-timesteps.json`, adds the three meaningful tests in the existing DDPM test class, and runs `verify empty-timesteps --phase baseline` before editing implementation. The intended failure is an `IndexError` from the original source. It then applies the small guard and uses upstream `utils/check_copies.py --fix_and_overwrite` to refresh the marked parallel copy. `verify empty-timesteps --level full` calls the pinned tests and upstream quality checks; `report empty-timesteps` writes the shared review page, Markdown, PR draft and patch under `.ramp/empty-timesteps/`.

For a fresh rehearsal, make another clone of the reviewed `ramp-base` branch on a clean engineer host. Do not reset or clean a checkout containing someone's work. Completed contributions and kit verification fixtures stay on the separate owner/reviewer host; do not make them available to the new Cursor session.

To extend this to another input-validation task, choose the owning API and its tests, update the profile's approved references and edit paths, then create a task spec with concrete criteria and mapped test IDs. Run `doctor`, reproduce the regression on original implementation and verify the changed behaviour. New semantics or a different component may require new recipe code and tests; changing profile data alone does not establish support.

## Reading the result

`READY_FOR_HUMAN_REVIEW` means the pinned local full checks passed and the intended regression was observed against the original implementation (pre-implementation baseline and later replay are separately labelled). It is not remote CI, maintainer approval, package publication or deployment. PM validates the outcome and criteria; QA inspects baseline and candidate tests; DevOps checks the fork CI run and release process. A changed source, task, assessment, policy or environment makes prior candidate evidence stale. Human review remains required for the patch and all proposed PR wording.

The business hypothesis is shorter time to the first useful patch and fewer reviewer correction cycles. For a pilot, record elapsed time from first request to passing candidate, reviewer correction count, and first-pass acceptance rate against a comparable baseline. This one local rehearsal is technical evidence, not a measured business improvement.

See `DEMO.md` for the 8–12 minute interview journey and `DECISIONS.md` for design trade-offs and limitations.

See `RELEASE.md` for the two-stage fork CI setup and executable optional packaging commands; `MAINTENANCE.md` for profile updates and a second-task extension example; `CURSOR-REHEARSAL.md` for the remaining runtime acceptance check.
