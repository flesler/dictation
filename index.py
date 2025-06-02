import runner
import recorder
import microphone
import os
import sys
import psutil
import argparse
import time
import signal
import subprocess

def process(text):
  text = runner.process(text)
  if args.single:
    stop()
  return text

def check_another():
  current_pid = os.getpid()
  script_name = os.path.basename(__file__)

  for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
      if proc.info['pid'] == current_pid:
        continue
      cmdline = proc.info.get('cmdline') or []
      # Check if 'python' in name and 'index.py' in cmdline
      if (
        ('python' in (proc.info['name'] or '').lower() or any('python' in c for c in cmdline))
        and any(script_name in c for c in cmdline)
      ):
        # Kill the other process and exit
        proc.send_signal(signal.SIGTERM)
        print("Killed another running index.py process. Exiting this instance.")
        play('cockchafer-gentleman-1') # pisk-down
        sys.exit(0)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      continue


def start():
  # Cache in this directory
  os.environ["HF_HOME"] = os.path.abspath("./downloads")
  recorder.start(args)
  # Ensure microphone is unmuted
  microphone.start()
  print('Ready')
  play('percussion-12')
  recorder.monitor(process)

def stop():
  recorder.stop()
  microphone.stop()
  play('percussion-28')

def play(file):
  subprocess.run(['paplay', f'/usr/share/sounds/sound-icons/{file}.wav'], stdout=subprocess.DEVNULL)

if __name__ == '__main__':
  # If another python with index.py is running, kill it and exit this
  check_another()
  # Listen for SIGTERM and exit
  def handle_signal(signum, frame):
    stop()
    sys.exit(0)
  signal.signal(signal.SIGTERM, handle_signal)

  parser = argparse.ArgumentParser(description="Start the voice recorder")
  parser.add_argument('--lang', type=str, default='en', help='Language code (e.g., en, es)')
  parser.add_argument('--single', action='store_true', help='If set, exits after one dictation')
  parser.add_argument('--polish', action='store_true', help='If set, sentences get punctuation and title case')
  args = parser.parse_args()
  start()
