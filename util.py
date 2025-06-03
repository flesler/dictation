import time

start_time = None

def time_start():
  global start_time
  start_time = time.time()

def time_end(name = 'operation'):
  global start_time
  end_time = time.time()
  print(f"{name} took {end_time - start_time:.3f} seconds")