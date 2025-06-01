import re

MAPPING = {
  # Punctuation:
  "dot": ".",
  "period": ".",
  "comma": ",",
  "coma": ",",
  "colon": ":",
  "semicolon": ";",
  "dash": "-",
  "minus": "-",
  "underscore": "_",
  "slash": "/",
  "backslash": "\\\\",
  "quote": "\"",
  "double quote": "\"",
  "apostrophe": "'",
  "single quote": "'",
  "left paren": "(",
  "right paren": ")",
  "open paren": "(",
  "close paren": ")",
  "left bracket": "[",
  "right bracket": "]",
  "open bracket": "[",
  "close bracket": "]",
  "left brace": "{",
  "right brace": "}",
  "open brace": "{",
  "close brace": "}",
  "less than": "<",
  "greater than": ">",
  "equals": "=",
  "plus": "+",
  "asterisk": "*",
  "percent": "%",
  "at": "@",
  "hash": "#",
  "pound": "#",
  "ampersand": "&",
  "pipe": "|",
  "caret": "^",
  "tilde": "~",
  "backtick": "`",
  "question mark": "?",
  "exclamation mark": "!",
  "bang": "!",
  # Whitespace:
  # "space": " ",
  # "tab": "\t",
  # "enter": "\n",
  # "new line": "\n",
  # Bad pronunciation:
  "workspace": "backspace",
  "countour": "control",
  # Add more mappings to fix case or skip filler words
  "usa": "USA",
  "u s a": "USA",
  "uk": "UK",
  "javascript": "JavaScript",
  "typescript": "TypeScript",
  "html": "HTML",
  "json": "JSON",
  "jason": "JSON",
  "sql": "SQL",
  "http": "HTTP",
  "https": "HTTPS",
  "ip": "IP",
  "url": "URL",
  "ram": "RAM",
  "api": "API",
  # TODO: Generate the spelling version letter by letter?
  "os": "OS",
  "ui": "UI",
  "cli": "CLI",
  "db": "DB",
  "dns": "DNS",
  "xml": "XML",
  "yaml": "YAML",
  "json": "JSON",
  "todo": "TODO",
  "github": "GitHub",
  "stackoverflow": "StackOverflow",
  # Filler words to skip
  "uh": "",
  "er": "",
  "ah": "",
  "huh": "",
  "hm": "",
  "um": "",
  # Shortcuts
  # "save": "control s",
  # "paste": "control v",
  # "copy": "control c",
  # "cut": "control x",
  # "undo": "control z",
  # "redo": "control y",
  # "comment": "control /",
  # "find": "control f",
  # "select all": "control a",
  # Hacks
  "clicked": "click",
  "kicked": "click",
  "clipped": "click",
  # Multi-word hotkeys
  "right click": "rightclick",
  "middle click": "middleclick",
  "wheel click": "middleclick",
  "page up": "pageup",
  "page down": "pagedown",
  "print screen": "printscreen",
  "volume up": "volumeup",
  "volume down": "volumedown",
  "volume mute": "volumemute",
  "mute": "volumemute",
  # Final polish
  "  ": " ",
  " .": ".",
  " ,": ",",
  " :": ":",
  " ;": ";",
  r"\r": r"\n",
  r"\n ": r"\n",
  r" \n": r"\n",
}

REGEX = re.compile(r"\b(" + "|".join(re.escape(k) for k in MAPPING) + r")\b", re.IGNORECASE)

def map(text):
  prev = None
  while prev != text:
    prev = text
    text = REGEX.sub(lambda x: map_word(x.group(1)), text)
  return tokenize(text)

def map_word(orig):
  key = orig.lower()
  repl = MAPPING[key]
  if orig and orig[0].isupper():
    return repl.capitalize()
  return repl

# Convert "Hello! how are you?" -> ["Hello", "! ", "how", " ", "are", " ", "you", "?"]
def tokenize(text):
  # This will match words or punctuation, possibly followed by spaces, commas, or periods
  return re.findall(r'\w+[ ,\.]*|[^\w\s,\.]+[ ,\.]*', text)