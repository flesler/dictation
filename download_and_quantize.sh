#!/bin/bash

# $ ./download_and_quantize.sh whisper-tiny.en int8
# Required: pip install transformers[torch]>=4.23

root=$(dirname $0)/downloads
mkdir -p $root

model=$1
quantization=${2:-int8}
# Match what the library expects
prefix='models--Systran--faster-'

ct2-transformers-converter --model openai/${model} --output_dir $root/${prefix}${model}-${quantization} --copy_files tokenizer.json preprocessor_config.json --quantization ${quantization}