# Reject empty custom timesteps with a clear error

## Why
As a library consumer, I want an empty custom timestep list to produce a clear ValueError while valid input and existing argument rules remain unchanged.

## What changed
Validate length in the existing custom-input branch after the mutual-exclusion check. This preserves valid lists and count-based scheduling. Propagate the marked parallel copy through the upstream copy tool and test both real schedulers.

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
