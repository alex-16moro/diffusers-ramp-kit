# Start here: move the kit into Cursor

The newcomer experience starts in a fresh Diffusers checkout. Keep this bundle, especially `deliverables/`, outside that Cursor workspace. The completed patch is reference evidence for the presenter; it must not be visible to the fresh development agent.

## 1. Prepare once, before the demo

The supported execution environment is Linux x86-64, Python 3.12, CPU Torch 2.7.1. Cursor can be on another computer, but its project terminal must use that environment. Native macOS/Windows dependency installation has not been tested; use a Linux environment for the recorded reproduction. This bundle is run directly with `run.py`; it is not an installable PyPI package.

From the extracted `diffusers-ramp-kit` folder, with Git and Python 3.12 available, run:

```bash
# Use new paths. If these already exist, choose different names.
git clone https://github.com/huggingface/diffusers.git ../diffusers-reference
python3.12 run.py --repo ../diffusers-reference onboard --dest ../diffusers-onboarding
bash ../diffusers-onboarding/.ramp-kit/runtime/bootstrap.sh ../diffusers-onboarding
cd ../diffusers-onboarding
source .ramp-venv/bin/activate
python .ramp-kit/run.py --repo . doctor
```

`onboard` checks out the exact pinned commit on `ramp/first-contribution`, copies the runtime kit and Cursor rules, and omits untracked files, old evidence and completed solutions. It refuses an existing destination. The source clone may have a newer HEAD; the onboarding checkout always uses the profile's pinned revision. If the clone lacks the pinned commit, fetch that exact commit from the approved upstream and retry. The upstream remote is a source only; the eventual contribution destination is the user's fork.

Bootstrap downloads packages. Do it before the demo. Bootstrap explicitly selects `python3.12` (or `PYTHON=/path/to/python3.12`). If environment creation fails, install `python3.12-venv`, or create `.ramp-venv` with an already available `virtualenv` and rerun bootstrap. Do not spoof versions or use the recovered environment as cold-install evidence. See the generated `review-checks/final-integrity.json` for the latest executed checks. Once prepared, checks use local source/dependencies and offline Hugging Face settings. Those settings do not block arbitrary network traffic.

## 2. Open only `diffusers-onboarding` in a fresh Cursor Agent session

Record the absolute open folder, `git status --short`, and `git stash list`. Capture a screenshot showing that `.cursor/rules/ramp-entry.mdc` appears as Always Apply in Cursor's Rules view. Set the project interpreter to `.ramp-venv/bin/python`. Disable web/MCP/external retrieval for this rehearsal. Start a new chat without this build conversation, the ZIP, or `deliverables/` in context.

Give only this request:

> Make passing an empty custom timestep list produce a clear error while preserving valid inputs. Could we just replace an empty list with `[999]`?

The agent should discover the guidance, read source, push back on the suggested fallback with citations, prepare the task and tests, reproduce the failure, implement the fix, repair checks and present the report. You should not have to type every CLI command. If automatic discovery fails, record that as a failed runtime check before using `@ramp-entry` as a fallback; the fallback does not count as successful automatic discovery.

## 3. Record the runtime acceptance test

Use `CURSOR-REHEARSAL.md` to record the actual Cursor version and observed journey. The builder's CLI rehearsal passed. The exploratory Cursor run had setup deviations. A clean acceptance run is still pending; record it separately. Do not call the live demo ready until it passes.

Open `.ramp/empty-timesteps/review.html` for the shared handoff. PM reviews criteria; QA inspects test evidence; DevOps reviews CI and the release handoff. `READY_FOR_HUMAN_REVIEW` is local evidence, not approval, remote CI, or deployment.
