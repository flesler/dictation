class Stream:
  def __init__(self, items):
    self.items = list(items)

  def peek(self):
    return self.items[0] if self.items else None

  def next(self):
    return self.items.pop(0)

  def has(self):
    return bool(self.items)