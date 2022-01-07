from __future__ import annotations

import re
from typing import Dict, List, Literal

from src import ini
from src import music


def __get_label(label: str) -> str:
    name = ini.gui(label + '-name')
    colour = ini.gui(label + '-colour')
    return name + ':' + colour


DAYS: List[str] = [__get_label('day-0'), __get_label('day-1'), __get_label('day-2'), __get_label('day-3')]

PERIODS: Dict[int, str] = {}
PERIODS.update(dict.fromkeys([4, 5, 6], __get_label('dawn')))
PERIODS.update(dict.fromkeys([7, 8, 9, 10, 11, 12], __get_label('morning')))
PERIODS.update(dict.fromkeys([13, 14, 15, 16, 17], __get_label('afternoon')))
PERIODS.update(dict.fromkeys([18, 19, 20], __get_label('twilight')))
PERIODS.update(dict.fromkeys([21, 22, 23, 0, 1, 2, 3], __get_label('night')))


def get_day(timer: Clock) -> str:
    if 1 <= timer.day <= 3:
        return DAYS[timer.day]
    return DAYS[0]


def get_period(timer: Clock) -> str:
    return PERIODS[timer.hour]


def get_time(timer: Clock) -> str:
    return f'{timer.hour}:{timer.minute}'


class Clock:
    START_DAY = 1
    START_HOUR = 5
    START_MINUTE = 0
    __INTERVALS = [int(ini.timer('interval-short')), int(ini.timer('interval-long'))]
    __BELL_HOURS = tuple(int(h) for h in ini.timer('bell-hours').split(','))
    __RUMBLE_HOURS = tuple(int(h) for h in ini.timer('rumble-hours').split(','))

    __HOUR_DURATION = 60
    __DAY_MAX = 3

    def __init__(self, day: int = START_DAY, hour: int = START_HOUR, minute: int = START_MINUTE):
        self.day = day
        self.hour = hour
        self.minute = minute
        self.running = False
        self.end = False
        self.slow = 0

    def update_time(self) -> None:
        """
        The method moves forward the timer, one minute at a time, and executes checks on the times.
        """
        if self.end:
            return
        self.minute += 1
        if self.minute >= self.__HOUR_DURATION:
            self.hour = (self.hour + 1) % 24
            self.minute = 0
            self.__play_sounds()
            if self.hour == self.START_HOUR:
                self.day += 1
                self.__check_day()

    def __check_day(self) -> None:
        """
        Called at every day change.
        If the day would go over the maximum numbers, it stops the timer, otherwise it plays the transition sound.
        """
        if self.day > self.__DAY_MAX:
            self.__set_time(self.__DAY_MAX, (self.START_HOUR - 1) % 24, 0)
            self.end = True
        else:
            music.new_day()

    def __play_sounds(self) -> None:
        self.__play_clock()
        self.__play_rumble()

    def __play_clock(self) -> None:
        """
        Plays either the bells or the single clock tick, the former at the hours set in the .ini file, the latter
        every other hour.
        """
        if self.minute == 0 and self.hour in self.__BELL_HOURS:
            music.bells()
        elif self.minute == 0:
            music.tick()

    def __play_rumble(self) -> None:
        """ Plays the rumble sound at the hours set in the .ini file. """
        if self.minute == 0 and self.hour in self.__RUMBLE_HOURS and self.day == self.__DAY_MAX:
            music.rumble()

    def __set_time(self, day: int, hour: int, minute: int) -> None:
        """ Sets the time, no checks if the values are legal. """
        self.day = day
        self.hour = hour
        self.minute = minute
        self.running = False

    def set_time(self, time: ClockTime) -> None:
        """ Sets the time from a ClockTime instance. """
        self.__set_time(time.day, time.hour, time.minute)

    def un_pause(self, mode: Literal['switch', 'stop', 'run'] = 'switch') -> None:
        """
        If it's not the end, changes the running state of the clock as specified.
        If mode is 'switch', it switches the state.

        :param mode: one of 'switch', 'stop' and 'run'
        """
        if not self.end:
            if mode == "switch":
                self.running = not self.running
            elif mode == "stop":
                self.running = False
            else:
                self.running = True

    def cycle_millis(self) -> None:
        """ Cycles between the two states, normal (0) and slow (1). """
        self.slow = 1 - self.slow

    def get_interval(self) -> int:
        return self.__INTERVALS[self.slow]

    def reset(self) -> None:
        """ Resets the timer to its starting value, at non-running state and non-slow speed """
        self.__set_time(self.START_DAY, self.START_HOUR, self.START_MINUTE)
        self.end = False
        self.slow = 0
        music.stop()

    def forward(self) -> None:
        """
        If it's not the end and it's not the last hour, it stops the timer, un-slows it
        and moves the clock one hour forward
        """
        if not (self.hour == self.START_HOUR - 1 and self.day == self.__DAY_MAX) and not self.end:
            new_hour = (self.hour + 1) % 24
            new_day = self.day + 1 if new_hour == self.START_HOUR else self.day
            self.__set_time(new_day, new_hour, self.START_MINUTE)
            self.slow = 0
            music.stop()

    def backward(self) -> None:
        """ If it's not the end, it stops the timer, un-slows it and moves the clock one hour backward. """
        changed = False
        if self.minute != self.START_MINUTE and not self.end:
            self.__set_time(self.day, self.hour, self.START_MINUTE)
            changed = True
        elif not (self.hour == self.START_HOUR and self.day == self.START_DAY) and not self.end:
            new_hour = (self.hour - 1) % 24
            new_day = self.day - 1 if new_hour == self.START_HOUR - 1 else self.day
            self.__set_time(new_day, new_hour, self.START_MINUTE)
            changed = True
        if changed:
            self.slow = 0
            music.stop()


class ClockTime:
    _PATTERN = "^[1-3]\\.(?:[01][0-9]|2[0-3])\\.[0-5][0-9]$"

    def __init__(self, day: int, hour: int, minute: int):
        self.day = day
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f'Day {self.day}, hour {self.hour}, min {self.minute}'

    def __repr__(self):
        return f'{self.day}.{self.hour:02}.{self.minute:02}'

    def __eq__(self, other):
        if not isinstance(other, ClockTime):
            return False
        return self.day == other.day and self.hour == other.hour and self.minute == other.minute

    @classmethod
    def from_str(cls, string: str) -> ClockTime:
        if re.match(cls._PATTERN, string) is None:
            raise ValueError("Invalid string")

        values = string.split(".")
        return ClockTime(int(values[0]), int(values[1]), int(values[2]))
