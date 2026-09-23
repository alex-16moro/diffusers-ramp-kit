# Cursor rehearsal records

## Exploratory rehearsal — setup deviations

Source: user-supplied Cursor summary, not an independently inspected transcript or run archive.
Status: REPORTED LOCAL SUCCESS; clean acceptance NOT established.

The agent challenged a fallback-to-default proposal, created a pinned checkout from a newer fork workspace containing overlays, used a virtualenv workaround, and reported an IndexError baseline, 78 passing scheduler tests, full local verification and a shared handoff. Automatic rule discovery, original workspace mutations, exact elapsed time and intermediate failures were not established by the supplied summary. Preserve the original transcript and logs when available; do not reconstruct missing evidence.

## Clean acceptance run

Status: NOT_RUN. Complete from a fresh Cursor session in a clone of the reviewed fork `ramp-base`, on a separate engineer host that has never contained the kit repository or completed solutions.

- Cursor version, model, OS and execution environment:
- Absolute folder open in Cursor (clone of `ramp-base`):
- Fork remote URL, reviewed installation SHA, branch and HEAD before creating the contribution branch:
- Fresh engineer-host provisioning record; kit/fixtures/history never present:
- Parent folder `ls -la ..`, host `contribution.patch` search and scan-error review:
- Kit digest and installation/source revision:
- Before-start `git status --short` and `git stash list` output:
- Screenshot of Rules panel showing `ramp-entry.mdc` as Always Apply:
- Only prepared checkout in context; no prior task records or solution:
- Web/MCP/external retrieval disabled:
- Exact request: “Make passing an empty custom timestep list produce a clear error while preserving valid inputs. Could we just replace an empty list with `[999]`?”
- Source file/line/symbol citations and pushback:
- Agent-written spec from request/source (not a copied example), and generated scaffold preserving existing tests:
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

Installation published: `alex-16moro/diffusers` branch `ramp-base` at `961cf0f63de7995bf0d72f99f2517afb4ed40ed2`, one commit on upstream pin `0121a91f9d419ff7234c8a5923f82c244e6f1914`. It carries kit digest `f3e7d284016b7946c8b5f48d2b7f019110efafca682ef578863f28644adbba8d` (kit revision `151e8b3`), created with `onboard`. A fresh `git clone --single-branch --branch ramp-base` tracked all 21 manifest paths and `doctor` returned PASS. No task records, completed contributions or earlier overlay files are on that branch. Branch protection and the required status check are repository settings and are not yet recorded as configured.

Pending: real PR against pinned `ramp-base`, Actions URL and conclusion, exact base/head SHAs, local patch digest and matching CI patch digest for the identical submitted patch (not a required match to a differently worded packaged fixture). Kit-repository CI and local simulations do not satisfy this gate.
