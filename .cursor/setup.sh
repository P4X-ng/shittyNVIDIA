#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON_BIN:-python3}"

if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "error: required interpreter '$python_bin' was not found" >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$python_bin" -m venv .venv
fi

# Reuse a persistent virtualenv so repeated environment boots stay fast.
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .

echo "Environment ready."
echo "Activate it with: source .venv/bin/activate"
echo "Run tests with: python test_shitty_nvidia.py && python test_mappings.py && python test_basic.py"
echo "Optional kernel module work still needs Linux headers and make in nvidia_compat_module/."
