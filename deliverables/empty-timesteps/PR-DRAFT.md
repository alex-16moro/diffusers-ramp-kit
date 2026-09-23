# Reject empty custom timesteps with a clear error

## Why
As a library consumer, I want an empty custom timestep list to produce a clear ValueError while valid input and existing argument rules remain unchanged.

## What changed
Reject an explicitly empty custom schedule with a clear error at its owning API; preserve valid input and mutual-exclusion precedence.

## Validation
READY_FOR_HUMAN_REVIEW: Local required checks passed. Remote CI and human review are separate.
- acceptance: PASS
- scheduler-tests: PASS
- lint: PASS
- format: PASS
- upstream-quality: PASS
- copies: PASS
- dummies: PASS
- support-list: PASS
- forward-docstrings: PASS
- dependency-table: PASS
- dependencies: PASS
- test-strength: PASS

## Reviewer attention
Confirm error wording, input compatibility, and argument-error precedence.

DRAFT: a human must review and approve this exact wording before publication. Remote CI, human approval and deployment have not been established.

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
