# Clean Cursor acceptance: evaluator protocol

**Evaluator-only.** This file is never part of the generated installation: `attach` copies only `rampkit/`, `profiles/`, `recipes/`, `templates/`, `examples/`, `runtime/`, `cursor/` and `run.py`, and `tests/test_install.py` checks that it stays out. Do not copy it, its criteria or the evaluator's expected outputs onto the Cursor host, into the fork, or into any PR, issue or commit message on the fork.

Agreed between Claude and Codex in alex-16moro/diffusers-ramp-kit#4. Owner decisions: evaluate from a reviewed upgrade of `ramp-demo` in `alex-16moro/diffusers` (D1); the parallel test module stays non-editable (D3, deferred).

## Run classes

Every run is recorded as exactly one of these. Only the first is acceptance evidence.

| Class | Meaning |
|---|---|
| **Clean acceptance** | Every precondition below holds, the prompt is the agreed request verbatim, and there are zero interventions during the measured contribution. |
| **Assisted** | As above, but with any intervention (hint, correction, coaching, manual step). Log each one; the run is not acceptance. Example: alex-16moro/diffusers#25. |
| **Fixture rehearsal** | A known patch is replayed to exercise wiring, such as `scripts/reproduce.py`, alex-16moro/diffusers#23 or alex-16moro/diffusers#26. Never Cursor evidence. |
| **Staged failure** | A deliberately broken input used to test a failure path. Never acceptance; kept apart from all of the above. |

## Preconditions: do not launch until all hold

1. **Kit:** `main` carries the single final regeneration; `unit`, `manifest` and `integration` are all green on that commit. Record the commit and its `kit_sha256`.
2. **Installation:** `ramp-demo` has been upgraded through a reviewed PR built from that commit with `attach --publish-repo alex-16moro/diffusers --publish-base ramp-demo`. Its diff against the pin touches only installation paths, nothing under `src/` or `tests/`. Record the `ramp-demo` SHA and the installed `kit_sha256`; they must equal step 1's.
3. **Fork refs:** the ref scan below is recorded immediately before the run, with no hit.
4. **Fresh Cursor environment:** provisioned from `ramp-demo` alone; it has never held the kit repository, its history, `tests/fixtures/`, `deliverables/`, `historical/`, an earlier contribution checkout or this file. The cloud setup (`.cursor/environment.json`) ran `install` successfully and `doctor` passes.
5. **Evaluator material** (this file, the G2 expected arrays, probe workflows, #4) lives only outside that environment.

## Before the first prompt (AC-E1)

Record, in this order, with UTC timestamps:

```bash
git -C <checkout> rev-parse HEAD                 # must equal the ramp-demo SHA from precondition 2
git -C <checkout> status --porcelain             # must be empty
git -C <checkout> branch -a
git -C <checkout> log --oneline -3
python .ramp-kit/run.py --repo . doctor          # PASS
python -c 'import json;print(json.load(open(".ramp-kit/attachment.json"))["kit_sha256"])'
```

Also record the Cursor environment build/session ID, the model shown in Cursor, and that no `.ramp/<task>` directory exists yet.

### Ref scan (immediately before the run)

Run on an evaluator machine, never in the Cursor environment. It lists every branch and PR ref on the fork and reports any ref whose changes to the target files add zero-steps validation.

```bash
PIN=0121a91f9d419ff7234c8a5923f82c244e6f1914
FILES="src/diffusers/schedulers/scheduling_ddpm.py src/diffusers/schedulers/scheduling_ddpm_parallel.py tests/schedulers/test_scheduler_ddpm.py tests/schedulers/test_scheduler_ddpm_parallel.py"
git ls-remote https://github.com/alex-16moro/diffusers.git > refs-before-run.txt
git fetch https://github.com/alex-16moro/diffusers.git '+refs/heads/*:refs/scan/heads/*' '+refs/pull/*/head:refs/scan/pull/*'
for ref in $(git for-each-ref --format='%(refname)' refs/scan); do
  git diff "$PIN" "$ref" -- $FILES \
    | grep -nE '^\+.*(num_inference_steps[^=]*(<=|<|==) *[01]\b|must be (a )?positive|greater than (0|zero)|at least (1|one))' \
    && echo "HIT: $ref"
done
# Commit messages added on the fork after the pin (upstream history is excluded).
git log --format='%H %s%n%b' "^$PIN" $(git for-each-ref --format='%(refname)' refs/scan) \
  | grep -niE 'zero[- ]?(inference[- ]?)?steps|num_inference_steps *= *0' && echo "MENTION in commit messages"
```

Record `refs-before-run.txt`, the full scan output and the timestamp. **Any `HIT` blocks the run.** A `MENTION` without a hit is reported to the owner, who decides before launch.

Known before the first scan: the fixture branch `ramp-fixture/provenance-empty-timesteps` (alex-16moro/diffusers#26) contains no zero-steps validation, but its commit message and PR body name the zero-inference-steps task. The owner decides whether to close #26 and delete the two `ramp-fixture/*` branches before the run. Its provenance is preserved in #4 and in the run 37105896700 log.

## The prompt (AC-E2)

Paste exactly this, once, as the only message, and record it verbatim:

> Make requesting zero inference steps produce a clear, appropriate error while preserving valid scheduling behavior. Could we simply replace zero with one?

No step list, file names, commands, hints or follow-ups. If Cursor asks a question, record it. Any answer is an intervention.

## During the run

- **Timings (AC-E9):** first prompt; kit rule or recipe first opened; `assess` recorded; baseline recorded; first green `verify --level full`; `report`; PR opened; fork CI conclusion.
- **Interventions (AC-E8):** zero for clean acceptance. Log any intervention as `UTC time | who | exact content | why`, and relabel the run **assisted**. Setup done before the first prompt is recorded under preconditions, not as an intervention.
- **Preserve unedited (AC-E9):** the full transcript, terminal output, `.ramp/<task>/`, the PR and the CI log.

## Gating criteria

### Contribution

- **G1:** `num_inference_steps=0` raises `ValueError` naming the argument in `DDPMScheduler` and `DDPMParallelScheduler`, for all three spacings (`leading`, `trailing`, `linspace`). `linspace` is gating even though the designated regression uses `leading`.
- **G2:** valid counts 1, 2, 50 and 1000 give exactly the pinned implementation's timesteps, for all three spacings and both classes. The evaluator computes the expected arrays from the pin in an evaluator-only environment after the run; they are never placed in Cursor's context.
- **G3:** existing errors are unchanged: `num_inference_steps > num_train_timesteps`, passing both `num_inference_steps` and `timesteps`, and the custom-timesteps path.
- **G4:** the parallel copy is propagated with the upstream tool (`utils/check_copies.py --fix_and_overwrite`, with `.ramp-venv/bin` on `PATH`), and the `copies` check passes.
- **G5:** before any implementation change, the designated regression fails at baseline with `ZeroDivisionError` raised in an implementation file (`baseline_error: ZeroDivisionError`, default `leading` spacing). The order is shown by timestamps.
- **G6:** `verify --level full` passes all 12 checks, including `test-strength`, and `report` shows `READY_FOR_HUMAN_REVIEW`.
- **G7:** on the contribution PR into `ramp-demo`:
  - the kit `verify` job in "Ramp Kit contribution checks" succeeds. Unrelated upstream workflows (for example `size-label`, `trufflehog`) are classified separately and are not this conclusion;
  - `ci-provenance.json` contains the expected task with `level: full` and `status: PASS`;
  - `runner_kit_sha256` = `policy_installed_kit_sha256` = `candidate_installed_kit_sha256` = the reviewed final kit digest;
  - `policy_checkout_sha` = `pr_base_sha`;
  - `tested_checkout_parents` are exactly {base, head}, or a head-only checkout is explicitly reported as such;
  - `patch_base_sha` = `upstream_pin` = the pin, and the CI `patch_sha256` equals the local one;
  - all consistency flags are true. The flags are necessary, not sufficient.

### Process

- **AC-E1:** start capture and ref scan, as above.
- **AC-E2:** verbatim prompt, as above.
- **AC-E3:** the transcript shows Cursor finding the kit rule and recipe without being told where they are. This is judged from the transcript, not inferred from a successful CLI run.
- **AC-E4:** the recorded assessment cites actual sources and judges "replace zero with one". Silently substituting a different step count changes the caller's request, so a clear error is the expected judgment. The decision is recorded with `assess`.
- **AC-E8:** zero interventions.
- **AC-E9:** transcript, timings and evidence preserved unedited.

### Observed, not gating

Negative counts, test placement, and error-message wording quality. `None` is out of scope.

## Evidence sources and their meaning

- **Local evidence:** `verify`/`report` output and `.ramp/<task>/`. In CI the same CLI still prints `"remote_ci": "NOT_RUN"` and "Local required checks passed". That describes the CLI's own local-evidence status, not the Actions result. G7 is established only by the Actions job conclusion together with the provenance record.
- **CI provenance:** the `ramp-evidence` artifact, or, when artifacts cannot be downloaded, the complete JSON printed by the "Record which revisions were verified" step. Preserve the full JSON, the run ID and attempt, and the job/step permalink outside Cursor. Compare `patch_sha256` values, not the artifact archive checksum.
- **Not evidence for this run:** fixture run 37105896700 (alex-16moro/diffusers#26) proves only the provenance path for the earlier kit `7302662a…`. The clean run must establish its own digests.

## Outcome record

Publish one record in alex-16moro/diffusers-ramp-kit#4 with:
- the run class;
- the precondition values (kit commit and digest, `ramp-demo` SHA, scan output and time);
- the verbatim prompt, timings and intervention log;
- the G1–G7 and process results, each marked observed or not met, with its source;
- links to the PR and CI run.

A failure is reported as a failure; it is not re-labelled or re-run silently.
