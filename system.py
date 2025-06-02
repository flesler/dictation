import os
import sys
import psutil
import argparse
import signal
import subprocess

def kill_another(sig = signal.SIGTERM):
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
  subprocess.run(['paplay', f'/usr/share/sounds/sound-icons/{file}.wav'], stdout=subprocess.DEVNULL)

def on(sig, handler):
  signal.signal(sig, handler)

def parse_args():
  parser = argparse.ArgumentParser(description="Start the voice recorder")
  parser.add_argument('--lang', type=str, default='en', help='Language code (e.g., en, es)')
  parser.add_argument('--single', action='store_true', help='If set, exits after one dictation')
  parser.add_argument('--polish', action='store_true', help='If set, sentences get punctuation and title case')
  return parser.parse_args()
