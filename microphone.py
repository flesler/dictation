# Pointless, just to silence several warnings from pyaudio :S
import sounddevice
import pyaudio
import subprocess

code = 'numid=7'

def start():
  _set_state(1)

def stop():
  _set_state(0)

def _set_state(state):
  subprocess.run(['amixer', 'cset', code, str(state)], stdout=subprocess.DEVNULL)

def is_muted():
  result = subprocess.run(['amixer', 'cget', code], stdout=subprocess.PIPE, text=True)
  flag = result.stdout.split('=')[-1].strip()
  return flag == 'off'

def get_device_index(verbose=False):
  p = pyaudio.PyAudio()
  try:
    devices = []
    has_headset = False
    for i in range(p.get_device_count()):
      info = p.get_device_info_by_index(i)
      name = info['name'].lower()
      is_input = info['maxInputChannels'] > 0
      if is_input:
        if verbose:
          print(f'{i} is {name}, maxInputChannels: {info["maxInputChannels"]}')
        devices.append((i, name))
      if 'usb audio device' in name:
        has_headset = True

    if has_headset:
      for device in devices:
        # usb audio device is the mic yet fails if chosen, pulse works
        if 'pulse' in device[1]:
          return device[0]

    for device in devices:
      if 'sysdefault' in device[1]:
        return device[0]
    return None
  finally:
    p.terminate()

if __name__ == "__main__":
  index = get_device_index(verbose=True)
  print(f"Selected device index: {index}")