# Start here: clone the prepared fork branch

The engineer has one starting point: a fresh clone of the user-owned Diffusers fork's reviewed `ramp-base` branch. The platform owner creates that branch using [RELEASE.md](RELEASE.md) **on a separate host**. `onboard` and `attach` are platform-owner commands, not engineer setup steps.

## 1. Keep completed solutions off the Cursor host

Use a dedicated engineer host that has never contained the kit repository, its Git history, `tests/fixtures/contribution.patch`, `deliverables/`, `historical/`, or previous completed contribution checkouts. The kit repository intentionally contains full solution fixtures for repeatable platform-owner verification; it must not be cloned onto this host. A sibling folder, another Cursor window, `.cursorignore`, or an instruction not to read the solution is not a sufficient boundary.

If this host already contains that material, provision a fresh host before recording clean acceptance. Do not describe the current builder/reviewer host as clean. This is an operator preparation requirement, not whole-agent filesystem/network isolation enforced by the kit; that requirement remains UNMET.

## 2. Clone `ramp-base`, bootstrap, then open Cursor

The platform owner supplies the fork URL and reviewed installation commit SHA. Do not assume the branch exists until the owner publishes and verifies it. Linux x86-64, Python 3.12 and CPU Torch 2.7.1 are the supported execution environment; native macOS/Windows dependency installation is not verified. Cursor's project terminal must use that environment.

Replace the example values below with the supplied URL and SHA; choose a new destination:

```bash
FORK_URL=https://github.com/YOUR_ACCOUNT/diffusers.git
INSTALLATION_SHA=REPLACE_WITH_REVIEWED_RAMP_BASE_COMMIT
git clone --single-branch --branch ramp-base --no-tags "$FORK_URL" diffusers-onboarding
cd diffusers-onboarding
test "$(git rev-parse HEAD)" = "$INSTALLATION_SHA"
bash .ramp-kit/runtime/bootstrap.sh .
source .ramp-venv/bin/activate
python .ramp-kit/run.py --repo . doctor
```

Keep the branch history: `doctor` and regression replay need the pinned upstream ancestor. Do not use `--depth 1`. Fetch only `ramp-base`, not contribution branches or tags. The reviewed branch must contain only the upstream pin and approved installation changes, with no solution in its ancestry. Do not merge newer fork `main`, earlier overlays or previous task records into it.

Bootstrap downloads packages; complete it before the session. It selects `python3.12` (or `PYTHON=/path/to/python3.12`). If environment creation fails, install `python3.12-venv`, or use an already available `virtualenv` to create `.ramp-venv` and rerun bootstrap. No model weights are needed. Offline Hugging Face settings do not block arbitrary network traffic.

## 3. Record the clean starting state

Before opening Cursor, record these outputs in the operator's rehearsal evidence, outside the checkout:

```bash
pwd
git remote -v
git branch --show-current
git rev-parse HEAD
git status --short
git stash list
ls -la ..
find / -type f -name contribution.patch -print 2> /tmp/ramp-host-scan-errors.txt
```

The branch must be `ramp-base` at the supplied installation SHA, with no task or solution present. Inspect the parent listing and host search: there must be no kit clone or completed contribution elsewhere on the host. After a run, its own `.ramp/` output is expected; before starting, no `contribution.patch` should exist. Review scan permission errors with the host owner; an incomplete search is not proof of absence. Preserve the scan and host-provisioning record. Filename checks are supporting evidence, not a security sandbox or a guarantee against renamed solutions.

Open **only this clone** in a fresh Cursor window and Agent session. Record the absolute open folder, Cursor version, model and environment. Capture the Rules panel showing `ramp-entry.mdc` as Always Apply. Select `.ramp-venv/bin/python`. Disable web, MCP and external retrieval; do not supply the build conversation, reviewer feedback or completed evidence. The operator can create a new contribution branch from the recorded installation commit before the request.

Give only this request:

> Make passing an empty custom timestep list produce a clear error while preserving valid inputs. Could we just replace an empty list with `[999]`?

The agent should discover guidance, inspect source, push back with citations, **write its own task spec** from the request, add missing tests without replacing existing ones, reproduce the failure, implement the change, verify it and present the report. The example spec is schema guidance, not a ready-made task to copy. If discovery fails, record the failure before trying `@ramp-entry`; the fallback does not count as automatic discovery.

## 4. Record acceptance separately from exploratory evidence

Complete [CURSOR-REHEARSAL.md](CURSOR-REHEARSAL.md), including all run results/logs, the authored spec, elapsed time and interventions. The prior exploratory run and the fixture-driven CLI rehearsal do not establish this clean journey. Clean acceptance is still NOT_RUN until observed and recorded.

Open `.ramp/empty-timesteps/review.html` for the shared handoff. PM reviews criteria, QA inspects tests, and DevOps checks provenance and actual fork CI. `READY_FOR_HUMAN_REVIEW` is local evidence, not approval, remote CI or deployment. A real contribution PR must target this same `ramp-base`; see RELEASE.md. Compare local and CI digests for the identical patch, not necessarily the packaged fixture's digest if the agent writes a different valid implementation.
