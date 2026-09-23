# Reject empty custom timesteps with a clear error

**READY_FOR_HUMAN_REVIEW** — Local required checks passed. Remote CI and human review are separate.

## PM — requested outcome
As a library consumer, I want an empty custom timestep list to produce a clear ValueError while valid input and existing argument rules remain unchanged.

| Criterion | Expected behaviour | Evidence status |
|---|---|---|
| AC1 | Both DDPM implementations reject empty custom timesteps with a useful ValueError; argument-conflict errors retain precedence. | PASS |
| AC2 | Normal and single-element custom timesteps retain their values and CPU device. | PASS |
| AC3 | Passing both timestep arguments still raises the existing error. | PASS |
| AC4 | Existing count-based inference timesteps still work. | PASS |

Exclusions: No scheduler numerical-update changes; No new exports or dependencies; No automatic replacement of invalid input; No remote publication or deployment

Next action: confirm these criteria reflect the requested outcome. No business approval is recorded.

## Engineering — design and review
Assessment: COMPATIBLE (agent judgement).
Reject an explicitly empty custom schedule with a clear error at its owning API; preserve valid input and mutual-exclusion precedence.
Changed paths: src/diffusers/schedulers/scheduling_ddpm.py, src/diffusers/schedulers/scheduling_ddpm_parallel.py, tests/schedulers/test_scheduler_ddpm.py

Source references:
- `.ai/references/code_style.md`
- `docs/source/en/conceptual/philosophy.md`
- `src/diffusers/schedulers/scheduling_ddpm.py`

Review questions: Is the error contract appropriate? Do valid inputs and argument-error precedence remain unchanged?

## QA — criteria and tests
- AC1: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_empty_custom_timesteps`
- AC2: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_custom_timesteps_validation_preserves_valid_inputs`
- AC3: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_custom_timesteps_passing_both_num_inference_steps_and_timesteps`
- AC4: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_count_based_inference_timesteps_unchanged`

Pre-implementation baseline: EXPECTED_FAILURE.
Fix-removal replay: PASS.
The replay runs current tests against the pinned original implementation in a disposable snapshot. A PASS means the intended regression failed again.

| Check | Status | Duration | Log |
|---|---|---|---|
| acceptance | PASS | 4.736s | [acceptance log](runs/20260923T113017534455Z/acceptance.log) |
| scheduler-tests | PASS | 6.703s | [scheduler-tests log](runs/20260923T113017534455Z/scheduler-tests.log) |
| lint | PASS | 0.027s | [lint log](runs/20260923T113017534455Z/lint.log) |
| format | PASS | 0.023s | [format log](runs/20260923T113017534455Z/format.log) |
| upstream-quality | PASS | 6.673s | [upstream-quality log](runs/20260923T113017534455Z/upstream-quality.log) |
| copies | PASS | 1.346s | [copies log](runs/20260923T113017534455Z/copies.log) |
| dummies | PASS | 0.024s | [dummies log](runs/20260923T113017534455Z/dummies.log) |
| support-list | PASS | 0.019s | [support-list log](runs/20260923T113017534455Z/support-list.log) |
| forward-docstrings | PASS | 2.88s | [forward-docstrings log](runs/20260923T113017534455Z/forward-docstrings.log) |
| dependency-table | PASS | 0.151s | [dependency-table log](runs/20260923T113017534455Z/dependency-table.log) |
| dependencies | PASS | 4.54s | [dependencies log](runs/20260923T113017534455Z/dependencies.log) |
| test-strength | PASS | 4.717s | [test-strength log](runs/20260923T113017534455Z/test-strength.log) |

Not covered: arbitrary scheduler types, GPU execution, all input shapes and diffusion numerical correctness.
QA next action: inspect the failing baseline and passing candidate logs; replay any disputed criterion.

## DevOps — delivery handoff
- Upstream base: `0121a91f9d419ff7234c8a5923f82c244e6f1914`
- Current runner kit digest: `f3e7d284016b7946c8b5f48d2b7f019110efafca682ef578863f28644adbba8d`
- Installation digest: `f3e7d284016b7946c8b5f48d2b7f019110efafca682ef578863f28644adbba8d`
- Reference source: attachment.json at installation; locally editable, not an independent trust anchor
- Required full checks: 12; executed in candidate: 12.
- Only fork CI enforces policy integrity. Its base policy and workflow require maintainer protection.
- Current patch digest: `5380733056ba1589e9cfebe911013967d661c8c25102c4443833847587462995`
- Environment: `{'python': '3.12.14', 'torch': '2.7.1+cpu', 'pytest': '8.3.5', 'ruff': '0.9.10', 'huggingface-hub': '1.32.0', 'safetensors': '0.8.0'}`
- Remote CI: NOT_RUN. Additive workflow configured; inspect the actual fork PR job before promotion.
- Package build / isolated consumer smoke test: NOT_RUN (optional feature omitted).
- Human review / production deployment: NOT_RUN.
- Shared runner: `python .ramp-kit/run.py --repo . verify empty-timesteps --level full`
- Promotion: maintainer-approved fork CI, human review, then the team’s package/release procedure. See RELEASE.md in the kit bundle for executable build and smoke instructions.
- Rollback: redeploy the prior approved wheel and restore its dependency lock; verify the consumer health checks.

## Boundaries and limitations
- Context/path and patch-scope checks are enforced by the kit. Whole-agent filesystem and network isolation are UNMET.
- An external Cursor tool can access beyond these helpers unless an operator provides separate isolation. Disable external retrieval for the rehearsal.
- Fresh Cursor rule discovery and autonomous completion remain UNVERIFIED until the operator records a fresh-session rehearsal.
- Reports are snapshots. Run report again after edits; copied HTML cannot detect later filesystem changes.
- No human approvals are fabricated. Review all PR wording, commit text, error strings, docstrings and comments before publishing.

## Exact wording awaiting human approval

Approval: NOT_RUN. Read the complete contribution.patch as well as this conservative inventory.
All added/changed Python string literals and comments are listed, including test text.
Dynamically constructed text must also be checked in the patch; this is not a semantic completeness guarantee.

Proposed commit message (draft):

```text
Reject empty custom timesteps with a clear error
```

The PR title and body above are also drafts awaiting exact-wording approval.

### src/diffusers/schedulers/scheduling_ddpm.py:300 — string literal (including errors and test text)

````text
`timesteps` cannot be empty.
````

### src/diffusers/schedulers/scheduling_ddpm_parallel.py:315 — string literal (including errors and test text)

````text
`timesteps` cannot be empty.
````

### tests/schedulers/test_scheduler_ddpm.py:162 — string literal (including errors and test text)

````text
timesteps.*empty
````

### tests/schedulers/test_scheduler_ddpm.py:164 — string literal (including errors and test text)

````text
Can only pass one
````

### tests/schedulers/test_scheduler_ddpm.py:171 — string literal (including errors and test text)

````text
cpu
````

### tests/schedulers/test_scheduler_ddpm.py:173 — string literal (including errors and test text)

````text
cpu
````

### tests/schedulers/test_scheduler_ddpm.py:179 — string literal (including errors and test text)

````text
cpu
````

