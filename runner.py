import mapper
from stream import Stream
import controller
import os

def resume():
  global is_running
  is_running = True

def suspend():
  global is_running
  is_running = False

def repeat_hotkey():
  global last_hotkey
  controller.hotkey(*last_hotkey)

callbacks = {
  "click": controller.click,
  "rightclick": controller.right_click,
  "suspend": suspend,
  "resume": resume,
  "repeat": repeat_hotkey,
  # "undo": lambda: controller.hotkey(["control"], "z"),
  # "redo": lambda: controller.hotkey(["control"], "y"),
  "exit": lambda: sys.exit(0),
}

is_running = True
last_hotkey = None

def process(text):
  global last_hotkey
  stream = Stream(mapper.map(text))
  buffer = []
  modifiers = []
  token = None

  while stream.has():
    part = stream.next()
    prev_token = token
    token = ''.join(c for c in part.lower() if c.isalnum())

    print('part', part, 'token', token, 'prev_token', prev_token)
    # Don't treat as key if in the middle of a sentence
    can_be_key = controller.is_always_key(token) or modifiers or (not buffer and len(token) > 1)

    if can_be_key and token in callbacks and (is_running or token == "resume"):
      flush(buffer)
      callbacks[token]()
      continue

    if not is_running:
      continue

    if not token:
      # Non letters, just buffer
      buffer.append(part)
      continue

    if controller.is_modifier(token):
      modifiers.append(token)
      continue

    if not modifiers:
      # TODO: Make fancier, avoid flushing, turn to a character
      if token == 'enter':
        buffer.append('\n')
        continue
      if token == 'tab':
        buffer.append('\t')
        continue

    # (repeat) X times

    print('last_hotkey', last_hotkey, 'token', token, 'peek', stream.peek())
    if last_hotkey and token == 'times' and prev_token and prev_token.isdigit():
      buffer.pop()
      num = int(prev_token)
      for _ in range(num):
        repeat_hotkey()
      continue

    if can_be_key and controller.is_key(token):
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
