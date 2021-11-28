class ClockTime:
    def __init__(self, day: int, hour: int, minute: int):
        self.day = day
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f'--day {self.day} --hour {self.hour} --minute {self.minute}'

    def __repr__(self):
        return f'ClockTime({self.day}, {self.hour}, {self.minute})'

    def __eq__(self, other):
        if not isinstance(other, ClockTime):
            return False
        return self.day == other.day and self.hour == other.hour and self.minute == other.minute
