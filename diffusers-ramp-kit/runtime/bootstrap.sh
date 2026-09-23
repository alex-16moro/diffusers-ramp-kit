#!/usr/bin/env bash
# Bootstrap is networked. Verification uses local dependencies and HF offline settings.
set -euo pipefail
REPO=$(cd "${1:?Pass the Diffusers checkout}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), "Use Python 3.12"'
python3 -m venv "$REPO/.ramp-venv"
printf '*\n' > "$REPO/.ramp-venv/.gitignore"
PY="$REPO/.ramp-venv/bin/python"
"$PY" -m pip install 'torch==2.7.1+cpu' --index-url https://download.pytorch.org/whl/cpu
"$PY" -m pip install -r "$HERE/requirements.lock"
"$PY" -m pip install --no-deps --no-build-isolation -e "$REPO"
"$PY" -c 'import torch; assert torch.version.cuda is None; print(torch.__version__)'
