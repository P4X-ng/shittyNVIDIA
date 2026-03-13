#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON_BIN:-python3}"

if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "error: required interpreter '$python_bin' was not found" >&2
  exit 1
fi

install_venv_support() {
  local python_version
  python_version="$("$python_bin" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

  if ! command -v apt-get >/dev/null 2>&1; then
    echo "error: python venv support is missing and apt-get is unavailable" >&2
    exit 1
  fi

  if command -v sudo >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3-venv || sudo apt-get install -y "python${python_version}-venv"
  else
    apt-get update
    apt-get install -y python3-venv || apt-get install -y "python${python_version}-venv"
  fi
}

if [ ! -d ".venv" ]; then
  if ! "$python_bin" -m venv .venv; then
    rm -rf .venv
    install_venv_support
    "$python_bin" -m venv .venv
  fi
fi

# Reuse a persistent virtualenv so repeated environment boots stay fast.
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .

echo "Environment ready."
echo "Activate it with: source .venv/bin/activate"
echo "Run tests with: python test_shitty_nvidia.py && python test_mappings.py && python test_basic.py"
echo "Optional kernel module work still needs Linux headers and make in nvidia_compat_module/."
