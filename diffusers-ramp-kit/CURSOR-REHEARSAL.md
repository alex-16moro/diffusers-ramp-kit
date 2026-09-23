# Cursor rehearsal records

## Exploratory rehearsal — setup deviations

Source: user-supplied Cursor summary, not an independently inspected transcript or run archive.
Status: REPORTED LOCAL SUCCESS; clean acceptance NOT established.

The agent challenged a fallback-to-default proposal, created a pinned checkout from a newer fork workspace containing overlays, used a virtualenv workaround, and reported an IndexError baseline, 78 passing scheduler tests, full local verification and a shared handoff. Automatic rule discovery, original workspace mutations, exact elapsed time and intermediate failures were not established by the supplied summary. Preserve the original transcript and logs when available; do not reconstruct missing evidence.

## Clean acceptance run

Status: NOT_RUN. Complete from a fresh Cursor session after installing the corrected kit.

- Cursor version, model, OS and execution environment:
- Absolute folder open in Cursor:
- Kit digest and installation/source revision:
- Before-start `git status --short` and `git stash list` output:
- Screenshot of Rules panel showing `ramp-entry.mdc` as Always Apply:
- Only prepared checkout in context; no prior task records or solution:
- Web/MCP/external retrieval disabled:
- Exact request: “Make passing an empty custom timestep list produce a clear error while preserving valid inputs. Could we just replace an empty list with `[999]`?”
- Source file/line/symbol citations and pushback:
- Agent-written spec and generated mapped scaffold:
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

Pending: real PR against pinned `ramp-base`, Actions URL and conclusion, exact base/head SHAs, local patch digest and matching CI patch digest. Kit-repository CI and local simulations do not satisfy this gate.
