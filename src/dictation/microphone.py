# Pointless, just to silence several warnings from pyaudio :S
import sounddevice
import pyaudio
import subprocess
import sys
from . import system

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

def get_devices():
  p = pyaudio.PyAudio()
  try:
    devices = []
    for i in range(p.get_device_count()):
      info = p.get_device_info_by_index(i)
      name = info['name']
      is_input = info['maxInputChannels'] > 0
      if is_input:
        devices.append((i, name))
    return devices
  finally:
    p.terminate()

def get_device_index():
  devices = get_devices()
  mic_name = system.args.microphone
  
  # Try to find device with the specified name
  for index, device_name in devices:
    if mic_name.lower() in device_name.lower():
      return index
  
  # If not found, print available devices and exit
  print("Available microphone devices:")
  for index, device_name in devices:
    print(f"  {index}: {device_name}")
  print(f"\nMicrophone '{mic_name}' not found.")
  print("Use --microphone <name> to specify a different device.")
  sys.exit(1)
