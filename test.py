import mapper
import runner
import time
import recorder
import system
import util

# time.sleep(1)
# runner.process("Hello! how are you? Control a Ctrl C Ok exit")

# print(mapper.map("Hello! Enter How are you? Tab Ok"))

system.parse_args()
util.time_start()
recorder.start()
util.time_end()
print(recorder.text())
recorder.stop()

util.time_start()
recorder.start()
util.time_end()
print(recorder.text())
recorder.stop()