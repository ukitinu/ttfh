from src import music
from src import ini


class Timer:
    START_DAY = 1
    START_HOUR = 5
    START_MINUTE = 0
    __INTERVALS = [int(ini.get_timer('interval-short')), int(ini.get_timer('interval-long'))]  # [2000, 3000]
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
        self.fast = 0

    def update_time(self) -> None:
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
        if self.minute == 0 and self.hour in self.__BELL_HOURS:
            music.bells()
        elif self.minute == 0:
            music.tick()

    def __play_rumble(self) -> None:
        if self.minute == 0 and self.hour in self.__RUMBLE_HOURS and self.day == self.__DAY_MAX:
            music.rumble()

    def __set_time(self, day: int, hour: int, minute: int) -> None:
        self.day = day
        self.hour = hour
        self.minute = minute

    def un_pause(self) -> None:
        if not self.end:
            self.running = not self.running

    def cycle_millis(self) -> None:
        self.fast = 1 - self.fast

    def get_interval(self) -> int:
        return self.__INTERVALS[self.fast]

    def reset(self) -> None:
        self.__set_time(self.START_DAY, self.START_HOUR, self.START_MINUTE)
        self.running = False
        self.end = False
        music.stop()
