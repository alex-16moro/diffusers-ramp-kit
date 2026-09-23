# Diffusers Contribution Ramp Kit

An agent-facing, repository-installed workflow for a first reviewable Diffusers contribution. Its supported example is rejecting an empty custom timestep list in `DDPMScheduler.set_timesteps` at pinned commit `0121a91f9d419ff7234c8a5923f82c244e6f1914`. The kit supplies scoped context, a task record, design assessment, a regression scaffold, local checks, and a shared PM/QA/DevOps handoff. Cursor remains the coding agent.

**Start with [START_HERE.md](START_HERE.md).** It contains the exact clean-checkout setup and the single request to give Cursor. See [FINAL-REVIEW.md](FINAL-REVIEW.md) for the requirement scorecard.

## Bootstrap and attach

1. Check out the pinned upstream commit in a disposable Diffusers worktree. Preserve any existing worktree and upstream instructions.
2. Use Python 3.12 on Linux x86-64. Run `bash runtime/bootstrap.sh /absolute/path/to/diffusers` while dependencies can be downloaded, then activate that checkout's `.ramp-venv`.
3. From this kit directory, run `python run.py --repo /absolute/path/to/diffusers doctor`, then `python run.py --repo /absolute/path/to/diffusers attach`.
4. Open the checkout in a fresh Cursor session. Ask: “Make passing an empty custom timestep list produce a clear error. Could we just replace it with `[999]`?” The always-on Cursor rule leads the agent through the recipe. An engineer need not hand-author the JSON or commands.

The attachment appends narrowly scoped exceptions to `.gitignore` so plain `git add -A` includes its rules, and adds `.ramp-kit/`, two `.cursor/rules/` files, `.cursorignore`, and an additive fork CI workflow. It refuses conflicting files and does not replace `AGENTS.md`, `.ai/`, or inherited workflows. Run `python .ramp-kit/run.py --repo . doctor` from the Diffusers root to diagnose drift. The kit only reads its approved source paths through `context`; it checks edits against the task's allowlist. These checks are not whole-agent filesystem or network isolation.

## Workflow and reset

The agent reads upstream instructions, approved context and the recipe, then records its assessment with `assess`. The proposed `[999]` fallback conflicts with the user's requested behaviour; an empty list should raise a clear `ValueError` in the owning scheduler API. A `REVISE` assessment can record that pushback before a `COMPATIBLE` assessment records the selected plan. The agent writes a new spec under `.ramp/specs/` from the request, using the example only as a schema guide. The agent runs `prepare --spec .ramp/specs/empty-timesteps.json`, adds the three meaningful tests in the existing DDPM test class, and runs `verify empty-timesteps --phase baseline` before editing implementation. The intended failure is an `IndexError` from the original source. It then applies the small guard and uses upstream `utils/check_copies.py --fix_and_overwrite` to refresh the marked parallel copy. `verify empty-timesteps --level full` calls the pinned tests and upstream quality checks; `report empty-timesteps` writes the shared review page, Markdown, PR draft and patch under `.ramp/empty-timesteps/`.

For a fresh rehearsal, create another worktree from the pinned upstream commit and attach the kit there. Do not reset or clean a worktree containing someone's edits. Keep the completed patch and its evidence in a separate worktree; the prepared onboarding state must not show the solution to the new Cursor session.

To extend this to another input-validation task, choose the owning API and its tests, update the profile's approved references and edit paths, then create a task spec with concrete criteria and mapped test IDs. Run `doctor`, reproduce the regression on original implementation and verify the changed behaviour. New semantics or a different component may require new recipe code and tests; changing profile data alone does not establish support.

## Reading the result

`READY_FOR_HUMAN_REVIEW` means the pinned local full checks passed and the intended regression was observed against the original implementation (pre-implementation baseline and later replay are separately labelled). It is not remote CI, maintainer approval, package publication or deployment. PM validates the outcome and criteria; QA inspects baseline and candidate tests; DevOps checks the fork CI run and release process. A changed source, task, assessment, policy or environment makes prior candidate evidence stale. Human review remains required for the patch and all proposed PR wording.

The business hypothesis is shorter time to the first useful patch and fewer reviewer correction cycles. For a pilot, record elapsed time from first request to passing candidate, reviewer correction count, and first-pass acceptance rate against a comparable baseline. This one local rehearsal is technical evidence, not a measured business improvement.

See `DEMO.md` for the 8–12 minute interview journey and `DECISIONS.md` for design trade-offs and limitations.

See `RELEASE.md` for the two-stage fork CI setup and executable optional packaging commands; `MAINTENANCE.md` for profile updates and a second-task extension example; `CURSOR-REHEARSAL.md` for the remaining runtime acceptance check.
