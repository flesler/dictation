import os
import sys
import psutil
import argparse
import signal
import subprocess
import time
from enum import Enum

args = None

class Sounds(Enum):
  BOOT = 'percussion-12'
  START = 'prompt' # canary-long
  STOP = 'percussion-28'
  FATAL = 'cockchafer-gentleman-1'

def kill_another(sig=signal.SIGTERM, attempts=3):
  current_pid = os.getpid()
  script_name = 'dictation'
  killed = False

  for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
      pid = proc.info['pid']
      if pid == current_pid:
        continue
      cmdline = proc.info.get('cmdline') or []
      if (
        ('python' in (proc.info['name'] or '').lower() or any('python' in c for c in cmdline))
        and any(script_name in c for c in cmdline)
      ):
        killed = True
        print(f"Sending SIGTERM to another process (pid={pid}).")
        for _ in range(attempts):
          proc.send_signal(sig)
          # Longer delay to allow buffer processing in --buffer mode
          time.sleep(2.5)
          if proc.is_running():
            print(f"Process (pid={pid}) did not exit, sending SIGKILL.")
            proc.send_signal(signal.SIGKILL)
          break
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      continue
  return killed

def play(file):
  if isinstance(file, Sounds):
    file = file.value
  # Use Popen to avoid blocking the main thread
  subprocess.Popen(['paplay', f'/usr/share/sounds/sound-icons/{file}.wav'], stdout=subprocess.DEVNULL)

def on(sig, handler):
  signal.signal(sig, lambda signum, frame: handler(signal.Signals(signum).name))

def abs_path(path):
  return os.path.abspath(path)

def parse_args():
  global args
  parser = argparse.ArgumentParser(description="Start the voice recorder")
  parser.add_argument('--lang', type=str, default='en', choices=['en', 'es'], help='Language code')
  parser.add_argument('--size', type=str, default='auto', help='Model size',
    choices=['auto', 'tiny', 'base', 'small', 'medium', 'large-v3', 'large-v3-turbo'])
  parser.add_argument('--quant', type=str, default='int8', help='quant type',
    choices=['none', 'int8', 'int16', 'float16', 'float32'])
  parser.add_argument('--microphone', type=str, default='pulse', help='Microphone device name')
  parser.add_argument('--wakeword', action='store_true', help='If set, the activation word is required')
  parser.add_argument('--single', action='store_true', help='If set, exits after one dictation')
  parser.add_argument('--stdout', action='store_true', help='If set, prints dictation to stdout')
  parser.add_argument('--tray', action='store_true', help='If set, shows a tray icon')
  parser.add_argument('--buffer', action='store_true', help='If set, buffers dictation until SIGTERM (push-to-talk mode)')
  args = parser.parse_args()
  
  if args.size == 'auto':
    # Used to only use this for wakeword and non-en, but now we use it for all
    args.size = 'large-v3-turbo'