from src import music
from src import ini


class Timer:
    START_DAY = 1
    START_HOUR = 5
    START_MINUTE = 0
    __INTERVALS = [int(ini.get_timer('interval-short')), int(ini.get_timer('interval-long'))]
    __BELL_HOURS = tuple(int(h) for h in ini.get_timer('bell-hours').split(','))
    __RUMBLE_HOURS = tuple(int(h) for h in ini.get_timer('rumble-hours').split(','))

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
            self.running = False
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

    def un_pause(self) -> None:
        """ If it's not the end, it switches the running state of the timer. """
        if not self.end:
            self.running = not self.running

    def cycle_millis(self) -> None:
        """ Cycles between the two states, normal (0) and slow (1). """
        self.slow = 1 - self.slow

    def get_interval(self) -> int:
        return self.__INTERVALS[self.slow]

    def reset(self) -> None:
        """ Resets the timer to its starting value, at non-running state and non-slow speed """
        self.__set_time(self.START_DAY, self.START_HOUR, self.START_MINUTE)
        self.running = False
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
            self.running = False
            self.slow = 0
            music.stop()
