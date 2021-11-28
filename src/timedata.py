from typing import Dict, List

from src import ini
from src.timer import Timer


def __get_label(label: str) -> str:
    name = ini.get_label(label + '-name')
    colour = ini.get_label(label + '-colour')
    return name + ':' + colour


DAYS: List[str] = [__get_label('day-0'), __get_label('day-1'), __get_label('day-2'), __get_label('day-3')]

PERIODS: Dict[int, str] = {}
PERIODS.update(dict.fromkeys([4, 5, 6], __get_label('dawn')))
PERIODS.update(dict.fromkeys([7, 8, 9, 10, 11, 12], __get_label('morning')))
PERIODS.update(dict.fromkeys([13, 14, 15, 16, 17], __get_label('afternoon')))
PERIODS.update(dict.fromkeys([18, 19, 20], __get_label('twilight')))
PERIODS.update(dict.fromkeys([21, 22, 23, 0, 1, 2, 3], __get_label('night')))


def get_day(timer: Timer) -> str:
    if 1 <= timer.day <= 3:
        return DAYS[timer.day]
    return DAYS[0]


def get_period(timer: Timer) -> str:
    return PERIODS[timer.hour]


def get_time(timer: Timer) -> str:
    return f'{timer.hour}:{timer.minute}'
