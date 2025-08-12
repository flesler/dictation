import sys
import signal
from . import cli


def main() -> None:
  cli.util.time_start('Boot')
  if cli.system.kill_another(signal.SIGTERM):
    sys.exit(0)

  cli.system.parse_args()

  cli.system.on(signal.SIGALRM, cli.on_signal)
  cli.system.on(signal.SIGINT, cli.on_signal)
  cli.system.on(signal.SIGTERM, cli.on_signal)

  if cli.system.args.tray:
    cli.tray.setup(cli.Colors.INACTIVE)

  cli.start()

if __name__ == "__main__":
  main()
