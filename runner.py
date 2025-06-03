import mapper
from stream import Stream
import controller
import os
import index
import time

def resume():
  global is_running
  is_running = True

def suspend():
  global is_running
  is_running = False

def repeat_hotkey():
  global last_hotkey
  controller.hotkey(*last_hotkey)

def submit():
  controller.hotkey([], "enter")
  time.sleep(0.05)
  index.stop()

callbacks = {
  "click": controller.click,
  "rightclick": controller.right_click,
  "suspend": suspend,
  "resume": resume,
  "repeat": repeat_hotkey,
  "exit": lambda: index.stop(),
  "quit": lambda: index.stop(),
  "shipit": submit,
}

is_running = True
last_hotkey = None
last_char = None

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

    # print('part', part, 'token', token)
    if token in callbacks and (is_running or token == "resume"):
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

    # (repeat) X times
    if last_hotkey and token == 'times' and prev_token and prev_token.isdigit():
      num = int(prev_token)
      # Don't risk a coloquialism like "1000 times"
      if num < 20:
        buffer.pop()
        for _ in range(num):
          repeat_hotkey()
        continue

    # Don't treat as key if in the middle of a sentence
    can_be_key = controller.is_always_key(token) or modifiers or (not buffer and len(token) > 1)
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
  
  return flush(buffer)

def flush(text):
  global last_char
  # print('flush', text, 'last_char "', last_char, '"')
  if not text:
    return
  if last_char and not is_space(last_char) and not is_space(text[0][0]):
    text.insert(0, " ")
  last_char = text[-1][-1]

  controller.paste(text)
  text.clear()
  return text

def is_space(char):
  return char == " " or char == "\n"