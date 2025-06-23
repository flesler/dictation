import runner
import recorder
import system
from system import Sounds
import microphone
import tray
from tray import Colors
import os
import sys
import signal
import util

# Needed to detect OOM errors, they happen on a thread
start_timeout = 3

def process(text):
  text = runner.process(text)
  if system.args.single:
    stop()
  return text

def on_signal(name):
  fatal(f"Received signal {name}")

def start():
  signal.alarm(start_timeout)
  try:
    # Ensure microphone is unmuted
    microphone.start()
    recorder.start()
    # Cancel alarm if successful
    signal.alarm(0)
  except Exception as e:
    fatal(e)
  
  system.play(Sounds.BOOT if system.args.wakeword else Sounds.START)
  util.time_end('Boot')
  if not system.args.wakeword:
    tray.set(Colors.ACTIVE)
  recorder.monitor(process)
  sys.exit(0)

def fatal(message):
  print(f"FATAL: {message}")
  stop(True)

def stop(force = False):
  microphone.stop()
  try:
    recorder.stop()
  except Exception as e:
    pass
  system.play(Sounds.FATAL if force else Sounds.STOP)
  if force:
    sys.exit(0)

if __name__ == '__main__':
  util.time_start('Boot')
  if system.kill_another(signal.SIGTERM):
    sys.exit(0)

  system.parse_args()

  system.on(signal.SIGALRM, on_signal)
  system.on(signal.SIGINT, on_signal)
  system.on(signal.SIGTERM, on_signal)

  if system.args.tray:
    tray.setup(Colors.INACTIVE)
  start()
