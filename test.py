import mapper
import runner
import time
import recorder
import system
import util

system.parse_args()
system.args.stdout = True

runner.process("Hello! How...")
runner.process("are.")
runner.process("you.")
runner.process("You good?")
runner.process("I hope well!")

# print(mapper.map("Hello! Enter How... are you? Tab Ok"))

# system.parse_args()
# util.time_start()
# recorder.start()
# util.time_end()
# print(recorder.text())
# recorder.stop()

# util.time_start()
# recorder.start()
# util.time_end()
# print(recorder.text())
# recorder.stop()