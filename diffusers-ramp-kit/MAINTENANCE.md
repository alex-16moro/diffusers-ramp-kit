# Maintaining and extending the profile

Ownership: upstream owns its source and conventions; the platform owner owns the pinned profile and kit; the task owns requested outcomes; executed checks own results. Architecture assessments remain agent judgement subject to human review.

## Updating Diffusers

1. Create a separate checkout of the proposed upstream SHA. Preserve the working demo.
2. Compare each approved path and relevant symbol against the old pin; review behaviour changes, renamed files, copy markers, tests and actual workflow commands. Do not merely replace hashes and infer semantic compatibility.
3. Run the chosen regression on the new untouched implementation. If upstream fixed it, retire the example and select/reproduce a nearby bounded validation task.
4. Update `profiles/diffusers.json`: SHA, approved-path hashes, symbols, edit scope, test modules and check commands. `doctor` checks hashes, symbol existence and check inputs. Refresh dependencies in a separate environment and test bootstrap.
5. Update the task spec, recipe and structural scaffold when their contracts change. Run kit tests, baseline reproduction, candidate full verification and a fresh Cursor rehearsal.
6. Review the kit diff and evidence, then approve a new installation commit on the fork. The CI base SHA pins that exact kit version. Keep the old pin and artifacts for rollback.

Upstream `AGENTS.md` is a symlink to `.ai/AGENTS.md` at this pin. Preserve it. The approved context helper uses `.ai/AGENTS.md` directly and continues to reject symlinks in requested paths.

## A second similar task

Example: “Reject an empty custom list after a schedule has already been configured, and preserve that previous schedule when validation fails.” Reuse the profile and recipe; copy `examples/empty-timesteps.json` to a new task spec with ID `empty-timesteps-preserve-state`. Change the request and AC1 to the state-preservation contract. The agent completes the structural regression method by configuring a valid schedule first, capturing it, then checking both the ValueError and unchanged state. Map that method to the revised criterion; do not reuse old test evidence. This is a worked extension plan, not a separately completed contribution.

Commands: `prepare --spec <new-spec>`, cited `assess`, baseline verification before the guard, candidate full verification and `report`. If source, requirements, checks or environment change, evidence is invalidated. New components or different error semantics may require new recipe code and tests.

## Boundaries

Approved bootstrap sources are the pinned Hugging Face Git repository, PyPI packages in `runtime/requirements.lock`, and the official PyTorch CPU package index for Torch. GitHub Actions acquisition is a CI setup dependency. No model weights or external retrieval are needed by the contribution check itself.

Context retrieval is restricted to profile paths and symbols; editable files come from the task/profile; commands come from the approved profile. Tests use local source and offline Hugging Face flags. These helpers reject traversal/symlinks and off-scope changes. They do not isolate the Cursor process or remove host credentials/network access: whole-agent isolation remains UNMET. The demonstration assumes a trusted operator and a dedicated checkout, not hostile code.
