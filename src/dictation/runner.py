from . import mapper
from . import system
from .stream import Stream
from . import controller
import os
from . import cli
import time
from . import recorder

def resume():
  global is_running
  is_running = True

def suspend():
  global is_running
  is_running = False

def repeat_hotkey():
  hotkey(*last_hotkey)

def submit():
  hotkey([], "enter")
  done()

def done():
  if system.args.wakeword:
    recorder.recorder.wake_word_activation_delay = 0.1
  else:
    time.sleep(0.05)
    cli.stop()

callbacks = {
  "click": controller.click,
  "rightclick": controller.right_click,
  "suspend": suspend,
  "resume": resume,
  "repeat": repeat_hotkey,
  "exit": lambda: cli.stop(),
  "quit": lambda: cli.stop(),
  "shipit": submit,
  "thatisit": done,
}

is_running = True
last_hotkey = None
last_char = None

def reset():
  global last_char
  last_char = None

def process(text):
  global last_hotkey
  if system.args.literal:
    return flush([text])
  orig = text
  text = mapper.map(text)
  stream = Stream(text)
  buffer = []
  modifiers = []
  token = None

  while stream.has():
    part = stream.next()
    prev_token = token
    token = to_token(part)

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
      modifiers.append(part)
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
      # Keep the original modifiers until last minute in case it's a false alarm
      mods = [to_token(m) for m in modifiers]
      last_hotkey = (mods.copy(), token)
      hotkey(mods, token)
      modifiers.clear()
      continue

    if modifiers:
      # False alarm
      buffer.extend(modifiers)
      modifiers.clear()

    buffer.append(part)

  return flush(buffer)

def flush(buffer):
  global last_char
  if not buffer:
    return

  text = ''.join(buffer)
  if last_char == "." and not text[0].islower():
    # Write the buffered dot
    text = ". " + text
    last_char = ' '

  if last_char and not is_space(last_char) and not is_space(text[0]):
    # Prepend a space in some cases
    text = " " + text

  last_char = text[-1]
  if last_char == ".":
    # Buffer the dot for the next pass
    text = text[:-1]

  if system.args.stdout:
    print(text, end="")
  else:
    controller.paste(text)
  buffer.clear()
  return text

def hotkey(modifiers, key):
  if system.args.stdout:
    print(" " + "+".join(modifiers) + "+" + key, end=" ")
  else:
    controller.hotkey(modifiers, key)

def is_space(char):
  return char == " " or char == "\n"

def to_token(text):
  return ''.join(c for c in text.lower() if c.isalnum())