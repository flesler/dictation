import runner
import recorder
import system
import microphone
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
  recorder.start()
  # Ensure microphone is unmuted
  microphone.start()
  system.play('percussion-12')
  util.time_end('Boot')
  recorder.monitor(process)

def stop(force = False):
  recorder.stop()
  microphone.stop()
  snd = 'cockchafer-gentleman-1' if force else 'percussion-28'
  system.play(snd)
  if force:
    sys.exit(0)

if __name__ == '__main__':
  util.time_start()
  system.parse_args()
  if system.kill_another(signal.SIGTERM):
    sys.exit(0)
  system.on(signal.SIGTERM, lambda signum, frame: stop(True))
  start()
