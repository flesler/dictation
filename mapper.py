import re

MAPPING = {
  "... ": ".",
  "...": ".",
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
  "backslash": "\\",
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
  "greater than equal": ">=",
  "less than equal": "<=",
  "less than": "<",
  "greater than": ">",
  "equals": "=",
  "plus": "+",
  "asterisk": "*",
  "percent": "%",
  # "at": "@",
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
  "enter": "\n",
  "new line": "\n",
  # Bad pronunciation:
  "ando": "undo",
  "dush": "dash",
  "dese": "these",
  "wax base": "backspace",
  "black space": "backspace",
  "block space": "backspace",
  "bug space": "backspace",
  "back space": "backspace",
  "clicked": "click",
  "kicked": "click",
  "clipped": "click",
  "control b": "control v",
  "control set": "control z",
  "workspace": "backspace",
  "contour": "control",
  # "do it": "repeat",
  "gtfo": "exit",
  "x it": "exit",
  "ext it": "exit",
  "our table": "Airtable",
  # Numbers
  "zero": "0",
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",
  "ten": "10",
  "eleven": "11",
  "twelve": "12",
  # Shortcuts
  "save it": "control s",
  "paste it": "control v",
  "copy it": "control c",
  "cut it": "control x",
  "undo it": "control z",
  "go back": "control z",
  "redo it": "control y",
  # "comment it": "control /",
  "find something": "control f",
  "find it": "f3",
  "select all": "control a",
  "select line": "press home shift end",
  # "select word": "press shift left",
  "scratch it": "control z",
  "go up": "press up",
  "go down": "press down",
  "go left": "press left",
  "go right": "press right",
  # Multi-word hotkeys
  "double click": "click click",
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
  "ship it": "shipit",
  "that's it": "thatisit",
  "that is it": "thatisit",
  # Filler words to skip
  "ah": "",
  "ahem": "",
  "er": "",
  "bbb": "",
  "mm-mm": "",
  "mmmmmmmm": "",
  "hm": "",
  "hmm": "",
  # "huh": "",
  "uh": "",
  "uwu": "",
  "um": "",
  "umm": "",
  "yep": "",
  "yup": "",
}

# Build regex for word-like keys
WORD_REGEX = re.compile(
  r"\b(" + "|".join(re.escape(k) for k in MAPPING if re.match(r'^[\w ]+$', k)) + r")\b",
  re.IGNORECASE
)
# Build regex for non-word keys
NONWORD_REGEX = re.compile(
  "(" + "|".join(re.escape(k) for k in MAPPING if not re.match(r'^[\w ]+$', k)) + ")",
  re.IGNORECASE
)

# print('WORD_REGEX', WORD_REGEX.pattern)
# print('NONWORD_REGEX', NONWORD_REGEX.pattern)

def map(text):
  prev = None
  while prev != text:
    prev = text
    text = WORD_REGEX.sub(lambda x: map_word(x.group(1)), text)
    text = NONWORD_REGEX.sub(lambda x: map_word(x.group(1)), text)
  # Remove spaces before some chars
  text = re.sub(r' +([\t\n ,.:;?!])', r'\1', text)
  # Remove spaces after some chars
  text = re.sub(r'([\n]) +', r'\1', text)
  # Remove spaces between contiguous numbers
  text = re.sub(r'(?<=\d)[ ,-]+(?=\d)', '', text)
  return tokenize(text)

def map_word(orig):
  key = orig.lower()
  repl = MAPPING[key]
  # print('map_word', orig, '->', repl)
  if orig and orig[0].isupper():
    return repl.capitalize()
  return repl

# Convert "Hello! how are you?" -> ["Hello", "! ", "how", " ", "are", " ", "you", "?"]
def tokenize(text):
  # Match single punctuation ("comma", "period")
  # |^[.,?!:-](?=[.,]?)$
  # This will match words or punctuation, possibly followed by spaces, commas, or periods
  return re.findall(r'\w+[ ,.:;?!]*|[\n\t]|[^\w\s,\.]+[ ,\.]*', text)