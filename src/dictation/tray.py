import pystray
from PIL import Image, ImageDraw
import threading
from enum import Enum

class Colors(Enum):
  INACTIVE = 'red'
  ACTIVE = 'green'

_tray = None
_thread = None

size = 32
width_ratio = 1.0 # .60

def _create_icon(color):
  image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(image)
  draw.rectangle((0, 0, image.width * width_ratio, image.height), fill=color)
  return image

def setup(color=Colors.INACTIVE, title="Dictation Status"):
  global _tray, _thread
  def _run():
    global _tray
    _tray = pystray.Icon("dictation")
    _tray.icon = _create_icon(color.value)
    _tray.title = title
    _tray.run()
  _thread = threading.Thread(target=_run, daemon=True)
  _thread.start()

def set(color):
  if _tray:
    _tray.icon = _create_icon(color.value)