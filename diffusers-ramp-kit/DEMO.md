# Live walkthrough (8–12 minutes)

1. **Engineer request (1 minute).** Open a fresh Cursor session on the prepared, pinned checkout and ask in ordinary language for a clear error on empty custom timesteps, suggesting `[999]`. Show automatic discovery of `.cursor/rules/ramp-entry.mdc` and the task recipe. Cursor runtime integration must be observed live; CLI checks alone do not establish that it works.
2. **Design and pushback (2 minutes).** Ask the agent to explain the owning method and cite the approved source and style guide. It should reject the silent `[999]` fallback, record `REVISE`, and adopt a small guard with a `COMPATIBLE` assessment. Show the assessment history. A maintainer decision is appropriate if the requester insists on changing the API contract.
3. **Baseline and contribution (3 minutes).** Show the prepared task and test scaffold. Add the regression, valid-input and count-based tests in the existing class. Run baseline verification and point to the actual `IndexError`, then let the agent make the guard and invoke Diffusers' copy tooling for the parallel scheduler.
4. **Review and repair (2 minutes).** Run fast, then full verification. The same task record maps criteria to tests; the kit invokes upstream checks. The baseline regression supplies the required real failure and diagnosis. Optionally introduce a disposable out-of-scope change, then remove it and rerun. Never edit the report to simulate green.
5. **Shared handoff (2 minutes).** Generate and open `review.html`. PM sees criteria, QA sees before/after test evidence, and DevOps sees local check commands and the boundary of release evidence. Inspect `contribution.patch` and the human-review PR draft. Explain that fork CI, human review and deployment remain separate.

Keep the Diffusers explanation brief: pipelines orchestrate inference, models predict, and schedulers select iterative update steps. This contribution validates an API input without changing the numerical update. Leave the rest of the 45-minute interview for design decisions, observed failures and questions.

## Rehearsal record

- Pinned commit: `0121a91f9d419ff7234c8a5923f82c244e6f1914`.
- CLI rehearsal: baseline reproduced `IndexError`; candidate full local verification passed; report said `READY_FOR_HUMAN_REVIEW`.
- Cursor version/session: **unverified in this environment**. Run this script in a fresh Cursor session and record the version, whether guidance was discovered without prompting, source citations, repair behaviour and elapsed time. Do not present the CLI rehearsal as a successful Cursor-agent test.
