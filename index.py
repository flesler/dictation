import runner
import recorder
import microphone
import os
import sys
import psutil
import argparse
import time

def process(text):
  runner.process(text)
  if args.single:
    stop()

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
        and any('index.py' in c for c in cmdline)
      ):
        # Kill the other process and exit
        proc.kill()
        print("Killed another running index.py process. Exiting this instance.")
        sys.exit(0)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      continue


# TODO: Bind to shortcut

def start():
  # Cache in this directory
  os.environ["HF_HOME"] = os.path.abspath("./downloads")
  # Ensure microphone is unmuted
  microphone.start()

  recorder.start(args.lang)
  print('Ready')
  recorder.monitor(process)

def stop(exit=True):
  recorder.stop()
  microphone.stop()
  if exit:
    time.sleep(0.5)
    sys.exit(0)

if __name__ == '__main__':
  # If another python with index.py is running, kill it and exit this
  check_another()
  parser = argparse.ArgumentParser(description="Start the voice recorder")
  parser.add_argument('--lang', type=str, default='en', help='Language code (e.g., en, es)')
  parser.add_argument('--single', action='store_true', help='If set, exits after one dictation')
  args = parser.parse_args()
  start()
