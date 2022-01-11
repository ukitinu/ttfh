from __future__ import annotations

import argparse
import logging
import sys

from src.graphics.window import Window
from src.timer import Clock

LOG = logging.getLogger(__name__)


def main(day: int, hour: int, minute: int, saves: str):
    """
    If the parameters are valid, it starts the clock.
    """
    if 1 <= day <= 3 and 0 <= hour <= 23 and 0 <= minute <= 59:
        LOG.info('Starting parameters: day %d, hour %d, minute %d', day, hour, minute)
        if saves:
            LOG.info('Starting savestate string: %s', saves)

        timer = Clock(day, hour, minute)
        window = Window(timer)
        window.create(saves)
    else:
        LOG.error('Invalid parameters: day %d, hour %d, minute %d', day, hour, minute)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('TTFH')
    parser.add_argument('--day', type=int, help='Starting day (1-3)', default=Clock.START_DAY, required=False)
    parser.add_argument('--hour', type=int, help='Starting hour (0-23)', default=Clock.START_HOUR, required=False)
    parser.add_argument('--minute', type=int, help='Starting minute (0-59)', default=Clock.START_MINUTE, required=False)
    parser.add_argument('--saves', type=str, help='Comma-separated saves', default='', required=False)
    args = parser.parse_args()
    main(args.day, args.hour, args.minute, args.saves)
