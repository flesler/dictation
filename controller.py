import pyautogui
import pyperclip
import time

def type(text):
  text = tostr(text)
  if not text:
    return
  # print('type', text)
  pyautogui.typewrite(text)

def is_modifier(key):
  return key in modifier_keys

def is_key(key):
  return key in pyautogui.KEYBOARD_KEYS

def is_always_key(key):
  return key in always_keys

def hotkey(modifiers, key):
  # Remove empty modifiers
  modifiers[:] = [w for w in modifiers if w]
  # return print('hotkey', modifiers, key)
  all_keys = [modifier_keys[m] for m in modifiers]
  all_keys.append(key)
  pyautogui.hotkey(*all_keys)

def click():
  pyautogui.click()

def right_click():
  pyautogui.click(button="right")

# Like type() but handles some special characters
def type_spanish(text):
  buffer = []
  text = tostr(text)
  for char in text:
    if char.lower() in spanish_specials:
      type(buffer)
      buffer = []
      pyperclip.copy(char)
      pyautogui.hotkey('ctrl', 'v')
      time.sleep(0.01) # Small delay to ensure paste works
    else:
      buffer.append(char)
  type(buffer)

def tostr(list_or_str):
  if isinstance(list_or_str, list):
    return "".join(list_or_str)
  return list_or_str

spanish_specials = set("áéíóúüñÁÉÍÓÚÜÑ")

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


# These don't need a modifier or "press" before them, to be used as keys instead of text
always_keys = {
  "tab", "slash", "backspace", "esc", "pageup", "pagedown", "printscreen", "volumeup", "volumedown", "volumemute", "win",
}

# print(pyautogui.KEYBOARD_KEYS)