from time import time

DEFAULT = 'operation'
_start = {}

def time_start(name=DEFAULT):
  _start[name] = time()

def time_end(name=DEFAULT):
  now = time()
  start = _start.get(name) or _start.get(DEFAULT)
  if start is None:
    raise KeyError(f"No start time found for '{name}'")
  print(f"{name} took {now - start:.3f} seconds")
  _start[name] = now