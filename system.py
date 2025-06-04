import os
import sys
import psutil
import argparse
import signal
import subprocess
from enum import Enum

args = None

class Sounds(Enum):
  BOOT = 'percussion-12'
  START = 'prompt' # canary-long
  STOP = 'percussion-28'
  FATAL = 'cockchafer-gentleman-1'

  current_pid = os.getpid()
  script_name = 'index.py'

  for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
      if proc.info['pid'] == current_pid:
        continue
      cmdline = proc.info.get('cmdline') or []
      if (
        ('python' in (proc.info['name'] or '').lower() or any('python' in c for c in cmdline))
        and any(script_name in c for c in cmdline)
      ):
        proc.send_signal(sig)
        print("Killed another running index.py process.")
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      continue
  return False

def play(file):
  if isinstance(file, Sounds):
    file = file.value
  # Use Popen to avoid blocking the main thread
  subprocess.Popen(['paplay', f'/usr/share/sounds/sound-icons/{file}.wav'], stdout=subprocess.DEVNULL)

def on(sig, handler):
  signal.signal(sig, handler)

def abs_path(path):
  return os.path.abspath(path)

def parse_args():
  global args
  parser = argparse.ArgumentParser(description="Start the voice recorder")
  parser.add_argument('--lang', type=str, default='en', choices=['en', 'es'], help='Language code')
  parser.add_argument('--size', type=str, default='small', help='Model size',
    choices=['tiny', 'base', 'small', 'medium', 'large-v3', 'large-v3-turbo'])
  parser.add_argument('--quant', type=str, default='int8', help='quant type',
    choices=['none', 'int8', 'int16', 'float16', 'float32'])
  parser.add_argument('--wakeword', action='store_true', help='If set, the activation word is required')
  parser.add_argument('--polish', action='store_true', help='If set, sentences get punctuation and title case')
  parser.add_argument('--single', action='store_true', help='If set, exits after one dictation')
  parser.add_argument('--stdout', action='store_true', help='If set, prints dictation to stdout')
  args = parser.parse_args()
