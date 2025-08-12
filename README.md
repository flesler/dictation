# dictation

Voice dictation with custom text mappings and keyboard/mouse shortcuts

## Features
- Real‑time speech‑to‑text with word/phrase remapping
- Inline command recognition (hotkeys like control s, enter, etc.)
- Optional tray icon and wake‑word mode
- Supports local CTranslate2 quantized Whisper models (int8) or non‑quantized

## Requirements
- Python 3.10+
- Linux audio (tested with PulseAudio)
- System deps: `paplay` (pulseaudio-utils)

## Setup
```bash
python -m venv venv
./venv/bin/pip install -U pip
./venv/bin/pip install -r requirements.txt
```

## Run
```bash
scripts/start.sh [--lang en|es] [--size auto|tiny|base|small|medium|large-v3|large-v3-turbo] \
  [--quant none|int8|int16|float16|float32] [--wakeword] [--single] [--stdout] [--tray] [--buffer]
```

Common examples:
```bash
# Fastest small model, quantized (requires local conversion below)
scripts/start.sh --size tiny

# Use non‑quantized model (downloads from HuggingFace cache)
scripts/start.sh --size tiny --quant none

# English tray icon
scripts/start.sh --tray --lang en
```

## Quantized model download (int8)
To use faster local models, convert with CTranslate2:
```bash
# Installs the converter in the venv if missing and converts into downloads/
scripts/download_and_quantize.sh tiny.en int8

# Other sizes
scripts/download_and_quantize.sh small.en int8
scripts/download_and_quantize.sh medium.en int8
scripts/download_and_quantize.sh large-v3-turbo int8
```
Converted models land in `downloads/<model>-<quant>/` and contain `model.bin`.

## Project layout
```text
src/
  dictation/
    __init__.py
    __main__.py     # python -m dictation
    cli.py          # main runtime logic
    controller.py   # key/mouse control
    microphone.py   # device selection
    mapper.py       # text/command mapping
    recorder.py     # audio loop + STT
    runner.py       # token processing
    stream.py
    system.py       # args, signals, sounds
scripts/
  start.sh
  download_and_quantize.sh
downloads/
  <models here>
```

## Development
- Module entrypoint: `python -m dictation` (scripts/start.sh sets `PYTHONPATH=src` for you)
- Prefer running via `scripts/start.sh`

## Troubleshooting
- CUDA OOM: use a smaller model (e.g., `--size tiny`) or `--quant int8`
- Missing `model.bin`: run the quantize script for the chosen size/quant, or use `--quant none`
- Audio device issues: set `--microphone` in `scripts/start.sh` args or adjust in `microphone.py`

## License
MIT
