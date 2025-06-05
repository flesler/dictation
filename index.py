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

def process(text):
  text = runner.process(text)
  if system.args.single:
    stop()
  return text

def start():
  try:
    # Ensure microphone is unmuted
    microphone.start()
    recorder.start()
  except Exception as e:
    print(f"Error starting recorder: {e}")
    system.play(Sounds.FATAL)
    sys.exit(1)
  system.play(Sounds.BOOT if system.args.wakeword else Sounds.START)
  util.time_end('Boot')
  if not system.args.wakeword:
    tray.set(Colors.ACTIVE)
  recorder.monitor(process)
  sys.exit(0)

def stop(force = False):
  recorder.stop()
  microphone.stop()
  system.play(Sounds.FATAL if force else Sounds.STOP)
  if force:
    sys.exit(0)

if __name__ == '__main__':
  util.time_start('Boot')
  system.parse_args()
  if system.kill_another(signal.SIGTERM):
    sys.exit(0)
  system.on(signal.SIGTERM, lambda signum, frame: stop(True))
  if system.args.tray:
    tray.setup(Colors.INACTIVE)
  start()
