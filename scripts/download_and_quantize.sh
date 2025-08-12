#!/usr/bin/env bash
# Usage: scripts/download_and_quantize.sh small.en int8

set -euo pipefail

model="${1:-}"
quant="${2:-int8}"

if [[ -z "$model" ]]; then
  echo "Usage: $(basename "$0") <model> [quant]" >&2
  exit 1
fi

if [[ "$quant" == *"_"* ]]; then
  echo "Error: quant cannot contain underscores (_)" >&2
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." &>/dev/null && pwd)"

# If venv exists, source it to get tools on PATH
if [[ -f "${REPO_ROOT}/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/venv/bin/activate"
fi


root="${REPO_ROOT}/downloads"
mkdir -p "$root"

CONVERTER="${REPO_ROOT}/venv/bin/ct2-transformers-converter"
if [[ ! -x "$CONVERTER" ]]; then
  CONVERTER=ct2-transformers-converter
fi

exec "$CONVERTER" \
  --model "openai/whisper-${model}" \
  --output_dir "${root}/${model}-${quant}" \
  --copy_files tokenizer.json preprocessor_config.json \
  --quantization "${quant}" \
  --force
