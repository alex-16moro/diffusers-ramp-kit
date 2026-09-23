# CI and release handoff

## What ran

The local runner passed the four mapped acceptance tests, both scheduler modules, Ruff checks, upstream quality/copy/dummy/support/docstring/dependency gates, and an original-implementation regression replay. Exact commands, exit codes, durations and logs are included under `deliverables/empty-timesteps/`. The replay PASS means the regression failed after the fix was removed; its inner pytest exit code is intentionally 1.

The check list comes from the pinned `.github/workflows/pr_tests.yml` repository-consistency job and dependency workflow. It does not claim to run every Makefile target or the full GPU suite. `make deps_table_check_updated` rewrites a generated table internally, so it runs in a disposable candidate snapshot. Formatting and copy propagation are separate developer operations.

## How fork CI is installed

Create a dedicated `ramp-base` branch at `0121a91f9d419ff7234c8a5923f82c244e6f1914` on the user-owned Diffusers fork. Do not attach to newer `main` or a worktree containing earlier overlays. Run `attach` from the reviewed kit. It adds narrow `.gitignore` exceptions for the two Cursor rules and uses `runtime/requirements.txt`; normal `git add -A` must retain all manifest paths. Inspect the staged files and manifest before committing under the applicable human-review rules. Clone the installation commit and run `doctor` before opening a contribution PR against `ramp-base`.

The repository-root `.github/workflows/test.yml` runs kit tests, the distribution manifest check, and the CLI integration rehearsal. Run the documented commands from the repository root. This workflow is separate from `templates/fork-ci.yml`, which is installed into a Diffusers checkout; kit CI is not evidence that a Diffusers fork PR has run.


This has two phases. A maintainer first reviews the vendored `.ramp-kit`, `.cursor/rules`, `.cursorignore`, and additive `.github/workflows/ramp-kit.yml` on the user-owned fork's base branch. The kit and manifest are versioned in that installation commit. A subsequent contribution PR includes its source/test changes plus `.ramp/<task>/task.json` and `architecture.json` (history/context index may also be included). The workflow checks out the exact PR base SHA for the trusted kit and uses it to verify the candidate; it does not download a moving kit branch or trust submitted green test evidence. It reruns baseline sensitivity itself.

The local and CI entry point is the same `run.py verify TASK --level full`; CI's runner path points to the copy on the approved base commit. Upstream workflows are preserved. The fork maintainer must protect the workflow/policy paths and require the check through repository settings; the kit does not configure GitHub protections. A PR cannot make its own edited workflow bypass-resistant by itself.

Diffusers fork CI is **configured, not yet demonstrated by a real fork PR**. A kit-repository CI run or local base-policy simulation does not satisfy this gate. Record the actual fork Actions URL, conclusion, exact base/head SHAs and patch digest; compare that digest with the local handoff for the identical patch. Patch generation uses full blob IDs and fixed diff formatting. The upstream fast-test workflow references organization-specific AWS runners and images that may not be available on a personal fork. The additive job uses hosted Ubuntu and the scoped CPU suite. This does not demonstrate all upstream jobs are runnable on that fork.

## Packaging and staging (optional, NOT RUN)

These are operator commands for a later packaging rehearsal, not completed evidence. Run them from the reviewed modified checkout on Linux with Python 3.12. They create separate build and consumer environments and do not replace the developer's environment. Package acquisition is a networked setup step; pre-cache it for an offline presentation.

```bash
set -euo pipefail
CONTRIBUTION_DIR=$(pwd)
STAGING_DIR=$(mktemp -d)
python3.12 -m venv "$STAGING_DIR/build-env"
"$STAGING_DIR/build-env/bin/python" -m pip install build
"$STAGING_DIR/build-env/bin/python" -m build --wheel --outdir "$STAGING_DIR/wheels" "$CONTRIBUTION_DIR"
WHEEL_PATH=$("$STAGING_DIR/build-env/bin/python" - "$STAGING_DIR/wheels" <<'PY'
from pathlib import Path
import sys
wheels = list(Path(sys.argv[1]).glob('*.whl'))
assert len(wheels) == 1, wheels
print(wheels[0].resolve())
PY
)
sha256sum "$WHEEL_PATH"
python3.12 -m venv "$STAGING_DIR/consumer"
"$STAGING_DIR/consumer/bin/python" -m pip install 'torch==2.7.1+cpu' --index-url https://download.pytorch.org/whl/cpu
"$STAGING_DIR/consumer/bin/python" -m pip install -r "$CONTRIBUTION_DIR/.ramp-kit/runtime/requirements.txt"
"$STAGING_DIR/consumer/bin/python" -m pip install --no-deps "$WHEEL_PATH"
cd "$STAGING_DIR"
"$STAGING_DIR/consumer/bin/python" -I - <<'PY'
from pathlib import Path
import sysconfig
import diffusers
from diffusers import DDPMScheduler, DDPMParallelScheduler
assert Path(diffusers.__file__).resolve().is_relative_to(Path(sysconfig.get_path('purelib')).resolve())
for cls in (DDPMScheduler, DDPMParallelScheduler):
    scheduler = cls()
    try:
        scheduler.set_timesteps(timesteps=[])
    except ValueError as exc:
        assert 'empty' in str(exc)
    else:
        raise AssertionError('Expected ValueError')
    scheduler.set_timesteps(timesteps=[999], device='cpu')
    assert scheduler.timesteps.tolist() == [999]
print('ISOLATED CONSUMER SMOKE PASSED', diffusers.__file__)
PY
```

Record the exact wheel hash, patch hash, kit digest, runtime, build output and smoke result before saying installability is verified. This run would simulate a staging consumer, not production deployment.

## Promotion and rollback

The maintainer reviews the exact patch and PR wording, checks the actual fork CI results, and chooses the team's normal package/version release procedure. DevOps promotes only the approved wheel and recorded dependency lock after the consumer smoke check and application-specific acceptance. PM accepts the criteria; QA reviews coverage and regression evidence. No approvals have been recorded by this kit.

Retain the previous approved wheel and dependency lock. Roll back by reinstalling that exact artifact in consumers and rerunning their health checks. No GitHub publication, package upload or production change was performed during this build.

## Regenerating evidence

From this kit directory, run the following into new disposable paths:

```bash
python3.12 scripts/reproduce.py --source /path/to/local-diffusers-clone --work /new/disposable/rehearsal --output /new/evidence
/new/disposable/rehearsal/.ramp-venv/bin/python scripts/export_evidence.py --run /new/evidence
sha256sum -c CONTENTS.sha256
```

The fixture-driven CLI run is explicitly labelled. The exporter preserves initial historical evidence unchanged, reruns kit tests/lint, publishes current results and rebuilds checksums. It refuses evidence from a different kit digest. Never manually change logs or generated result JSON to reflect intended outcomes.
