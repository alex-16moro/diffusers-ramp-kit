# Live workflow walkthrough (8–12 minutes)

Demonstrate the journey from a plain-language request to a reviewable contribution. Diffusers provides the real source and checks; the audience does not need diffusion mathematics, model inference or image generation.

Choose and announce the run class first. The empty-timesteps task is a **worked demonstration** already described by installed resources. It cannot prove unseen-task generalisation. Clean acceptance is a separate run governed by `ACCEPTANCE.md` on the evaluator host; preserve the existing NOT_RUN status until its conditions are observed. Never expose evaluator-only material to the contribution agent.

1. **Request and recipe selection (2 minutes).** Follow START_HERE.md with a reviewed `ramp-demo` installation and a fresh session. For the worked demonstration, ask: “Make passing an empty custom timestep list produce a clear error while preserving valid inputs. Could we just replace an empty list with `[999]`?” Show automatic rule discovery, selection of the scheduler-validation recipe and a brief explanation of scope. Record discovery failures and interventions honestly.
2. **Architecture review (2 minutes).** Show the agent inspect the owning API and applicable guidance, explain the consequence of the proposed fallback, and propose a compatible approach with source citations. Show the assessment history. Highlight the parallel copy as a dependency inside a bounded contribution, not a reason to scan the whole repository.
3. **Contribution and verification (3 minutes).** Show the agent author the task record, preserve mapped existing tests, add meaningful regression tests and observe the original failure before editing implementation. It makes the focused change, propagates the marked copy with upstream tooling and runs focused then full verification. The engineer should not have to write JSON or choose commands.
4. **Shared handoff (2 minutes).** Open the generated review page. PM checks the outcome and criteria; QA inspects before/after evidence and gaps; DevOps checks provenance and the actual CI result when available. Show the patch and draft PR wording for human review. Distinguish local verification, remote CI and human approval.
5. **Scope boundary (1 minute).** Explain what happens if a request needs a new API, dependency or unsupported component: the agent surfaces the impact and proposes a smaller contribution or reviewed extension. Describe this as policy unless actually exercised and recorded.

## Optional staged failure

After the walkthrough, use a separate disposable checkout to apply a DDPM-only partial fix, leaving the marked copy unchanged. Announce that it is staged. Show the failing check, copy propagation and rerun; preserve both records. Do not inject this into clean acceptance or pretend it was an autonomous mistake.

## Evidence and timing

Use `CURSOR-REHEARSAL.md` to record the run class, installation SHA, Cursor version/model, selected recipe, source-grounded assessment, baseline, candidate checks, report, elapsed time and interventions. Existing fixture and coached runs remain in their original categories. A CLI replay does not establish automatic Cursor discovery.

The reusable capability is the contribution recipe. This task is one illustration of it; a second independent task is still needed to demonstrate reuse. Measure time to a reviewable contribution and reviewer corrections in a pilot; do not claim an improvement without a comparison.
