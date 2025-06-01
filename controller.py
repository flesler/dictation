import pyautogui

def type(text):
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