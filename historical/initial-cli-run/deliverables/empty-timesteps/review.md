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
Validate length in the existing custom-input branch after the mutual-exclusion check. This preserves valid lists and count-based scheduling. Propagate the marked parallel copy through the upstream copy tool and test both real schedulers.
Changed paths: src/diffusers/schedulers/scheduling_ddpm.py, src/diffusers/schedulers/scheduling_ddpm_parallel.py, tests/schedulers/test_scheduler_ddpm.py

Source references:
- `.ai/references/code_style.md`
- `src/diffusers/schedulers/scheduling_ddpm.py`
- `src/diffusers/schedulers/scheduling_ddpm_parallel.py`

Review questions: Is the error contract appropriate? Do valid inputs and argument-error precedence remain unchanged?

## QA — criteria and tests
- AC1: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_empty_custom_timesteps`
- AC2: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_custom_timesteps_validation_preserves_valid_inputs`
- AC3: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_custom_timesteps_passing_both_num_inference_steps_and_timesteps`
- AC4: `tests/schedulers/test_scheduler_ddpm.py::DDPMSchedulerTest::test_count_based_inference_timesteps_unchanged`

Original implementation: EXPECTED_FAILURE.
Fix-removal replay: PASS.
The replay runs current tests against the pinned original implementation in a disposable snapshot. A PASS means the intended regression failed again.

| Check | Status | Duration | Log |
|---|---|---|---|
| acceptance | PASS | 4.578s | [acceptance log](runs/20260923T085800258844Z/acceptance.log) |
| scheduler-tests | PASS | 6.17s | [scheduler-tests log](runs/20260923T085800258844Z/scheduler-tests.log) |
| lint | PASS | 0.028s | [lint log](runs/20260923T085800258844Z/lint.log) |
| format | PASS | 0.031s | [format log](runs/20260923T085800258844Z/format.log) |
| upstream-quality | PASS | 6.145s | [upstream-quality log](runs/20260923T085800258844Z/upstream-quality.log) |
| copies | PASS | 1.473s | [copies log](runs/20260923T085800258844Z/copies.log) |
| dummies | PASS | 0.025s | [dummies log](runs/20260923T085800258844Z/dummies.log) |
| support-list | PASS | 0.021s | [support-list log](runs/20260923T085800258844Z/support-list.log) |
| forward-docstrings | PASS | 2.897s | [forward-docstrings log](runs/20260923T085800258844Z/forward-docstrings.log) |
| dependency-table | PASS | 0.148s | [dependency-table log](runs/20260923T085800258844Z/dependency-table.log) |
| dependencies | PASS | 4.733s | [dependencies log](runs/20260923T085800258844Z/dependencies.log) |
| test-strength | PASS | 4.887s | [test-strength log](runs/20260923T085800258844Z/test-strength.log) |

Not covered: arbitrary scheduler types, GPU execution, all input shapes and diffusion numerical correctness.
QA next action: inspect the failing baseline and passing candidate logs; replay any disputed criterion.

## DevOps — delivery handoff
- Upstream base: `0121a91f9d419ff7234c8a5923f82c244e6f1914`
- Kit content digest: `b334e02c36417d19a6d41c20c08cc413425d3ae373c73fb8c82681dd4522186b`
- Current patch digest: `f9b1cf957b42238c676255e2f0008af4067463c3cab51714634d171b0dba715c`
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
- No human approvals are fabricated. Review all PR wording before publishing.
