import runner
import recorder
import microphone
import os
import sys
import psutil

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

def start(lang=None):
  # Cache in this directory
  os.environ["HF_HOME"] = os.path.abspath("./downloads")
  # Ensure microphone is unmuted
  microphone.start()

  recorder.start(lang)
  print('Ready')
  recorder.monitor(runner.process)

def stop(exit=True):
  recorder.stop()
  microphone.stop()
  if exit:
    sys.exit(0)

if __name__ == '__main__':
  # If another python with recorder.py is running, kill it and exit this
  check_another()
  lang = None
  if len(sys.argv) > 1:
    lang = sys.argv[1]
  start(lang)
