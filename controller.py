import pyautogui
import pyperclip
import time

def type(text):
  text = tostr(text)
  if text:
    pyautogui.typewrite(text)

# Use paste instead of typing, works with tildes and ctrl-z undoes all
def paste(text):
  text = tostr(text)
  if text:
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

def is_modifier(key):
  return key in modifier_keys

def is_key(key):
  return key in pyautogui.KEYBOARD_KEYS or key in reverse_map

def is_always_key(key):
  return key in always_keys

def hotkey(modifiers, key):
  # Remove empty modifiers
  modifiers[:] = [w for w in modifiers if w]
  # return print('hotkey', modifiers, key)
  all_keys = [modifier_keys[m] for m in modifiers]
  key = reverse_map.get(key, key)
  all_keys.append(key)
  pyautogui.hotkey(*all_keys)

def click():
  pyautogui.click()

def right_click():
  pyautogui.click(button="right")

def tostr(list_or_str):
  if isinstance(list_or_str, list):
    return "".join(list_or_str)
  return list_or_str

modifier_keys = {
  "control": "ctrl",
  "ctrl": "ctrl",
  "shift": "shift",
  "alt": "alt",
  "meta": "meta",
  "super": "super",
  # "option": "option",
  # Forces anything after to be a shortcut
  "press": "",
}

reverse_map = {
  "\n": "enter",
  "\t": "tab",
}

# These don't need a modifier or "press" before them, to be used as keys instead of text
always_keys = {
  "tab", "slash", "backspace", "esc", "pageup", "pagedown", "printscreen", "volumeup", "volumedown", "volumemute", "win",
  "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
  "exit"
}

# print(pyautogui.KEYBOARD_KEYS)