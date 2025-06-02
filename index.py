import runner
import recorder
import microphone
import os
import sys
import system
import signal

def process(text):
  text = runner.process(text)
  if args.single:
    stop()
  return text

def start():
  # Cache in this directory
  os.environ["HF_HOME"] = os.path.abspath("./downloads")
  recorder.start(args)
  # Ensure microphone is unmuted
  microphone.start()
  print('Ready')
  system.play('percussion-12')
  recorder.monitor(process)

def stop(force = False):
  recorder.stop()
  microphone.stop()
  snd = 'cockchafer-gentleman-1' if force else 'percussion-28'
  system.play(snd)
  if force:
    sys.exit(0)

if __name__ == '__main__':
  if system.kill_another(signal.SIGTERM):
    sys.exit(0)
  system.on(signal.SIGTERM, lambda signum, frame: stop(True))
  args = system.parse_args()
  start()
