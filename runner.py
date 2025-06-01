import mapper
from stream import Stream
import controller

def resume():
  global is_running
  is_running = True

def suspend():
  global is_running
  is_running = False

def repeat():
  global last_hotkey
  controller.hotkey(*last_hotkey)

callbacks = {
  "click": controller.click,
  "rightclick": controller.right_click,
  "suspend": suspend,
  "resume": resume,
  "repeat": repeat,
}

is_running = True
last_hotkey = None

def process(text):
  global last_hotkey
  stream = Stream(mapper.map(text))
  buffer = []
  modifiers = []

  while stream.has():
    part = stream.next()
    token = ''.join(c for c in part.lower() if c.isalpha())

    print('part', part, 'token', token)

    if token in callbacks and (is_running or token == "resume"):
      flush(buffer)
      callbacks[token]()
      continue

    if not is_running:
      continue

    if not any(c.isalpha() for c in part):
      # Non letters, just buffer
      buffer.append(part)
      continue

    if controller.is_modifier(token):
      modifiers.append(token)
      continue

    if controller.is_key(token):
      # If there's no buffered text, or modifiers or some keys, always assume it's a shortcut
      if controller.is_always_key(token) or modifiers or (not buffer and len(token) > 1):
        flush(buffer)
        last_hotkey = (modifiers.copy(), token)
        controller.hotkey(modifiers, token)
        modifiers.clear()
        continue

    if modifiers:
      # False alarm
      buffer.extend(modifiers)
      modifiers.clear()

    buffer.append(part)
  
  flush(buffer)

def flush(text):
  if text:
    controller.type("".join(text))
    text.clear()
