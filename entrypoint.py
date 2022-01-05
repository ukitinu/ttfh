from __future__ import annotations

import argparse
import sys

from src.timer import Clock
from src.graphics.window import Window


def main(day: int, hour: int, minute: int):
    timer = Clock(day, hour, minute)
    window = Window(timer)
    window.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('TTFH')
    parser.add_argument('--day', type=int, help='Starting day (1-3)', default=Clock.START_DAY, required=False)
    parser.add_argument('--hour', type=int, help='Starting hour (0-23)', default=Clock.START_HOUR, required=False)
    parser.add_argument('--minute', type=int, help='Starting minute (0-59)', default=Clock.START_MINUTE, required=False)
    args = parser.parse_args()

    if 1 <= args.day <= 3 and 0 <= args.hour <= 23 and 0 <= args.minute <= 59:
        main(args.day, args.hour, args.minute)
    else:
        print('Starting time out of bounds')
        sys.exit(1)
