#!/bin/bash

# $ ./download_and_quantize.sh small.en int8
# Required: pip install transformers[torch]

model=$1
quant=${2:-int8}

if [[ "$quant" == *"_"* ]]; then
  echo "Error: quant cannot contain underscores (_)"
  exit 1
fi

root=$(dirname $0)/downloads
mkdir -p $root

ct2-transformers-converter --model openai/whisper-${model} --output_dir $root/${model}-${quant} --copy_files tokenizer.json preprocessor_config.json --quantization ${quant} --force