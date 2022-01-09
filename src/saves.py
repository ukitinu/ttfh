from __future__ import annotations

import re
from typing import List, Optional, Dict

_SAVES: Dict[str, SaveState] = {}


def create(name: str, day: int, hour: int, minute: int) -> None:
    """
    Creates a new SaveState with the given values, provided they are legal and the name is unique.
    :param name: save name
    :param day: save day
    :param hour: save hour
    :param minute: save minute
    """
    if not SaveState.is_name_valid(name):
        raise ValueError(f'"{name}" is invalid.\n{SaveState.NAME_RULES}')
    if not SaveState.is_time_valid(day, hour, minute):
        raise ValueError(f'{day} {hour}:{minute} is invalid.')
    save = SaveState(name, day, hour, minute)
    if name in _SAVES:
        raise ValueError(f'"{name}" already in use')
    _SAVES[name] = save


def get_list() -> List[str]:
    """
    :return: returns a list with all the saves' names
    """
    return list(_SAVES.keys())


def get(name: str) -> Optional[SaveState]:
    """
    :param name: name of the save
    :return: save with the given name, or None
    """
    return _SAVES.get(name, None)


def delete(name: str) -> None:
    """
    Deletes the save with the given name
    :param name: name of the save to delete
    """
    _SAVES.pop(name, None)


def serialize() -> str:
    """
    Converts the saves to a comma-separated string, that can be later deserialised
    :return: string representing all the saves in memory
    """
    save_list = [repr(save) for save in _SAVES.values()]
    return ','.join(save_list)


def deserialize(string: str) -> None:
    """
    Deserialise the given string, storing the values in memory.
    It expects a string of comma-separated repr(SaveState), for example the one returned by the serialize() method.
    :param string: string to deserialise
    """
    values = string.split(',')
    for value in values:
        if value:
            save = SaveState.from_str(value)
            _SAVES[save.name] = save


class SaveState:
    NAME_LEN = 16
    _NAME_PAT = "[a-zA-Z0-9 ]{1," + str(NAME_LEN) + "}"
    _TIME_PAT = "[1-3]\\.(?:[01][0-9]|2[0-3])\\.[0-5][0-9]"
    _PATTERN = "^" + _NAME_PAT + "@" + _TIME_PAT + "$"
    NAME_RULES = "Rules:\n - length 1 to 16;\n - allowed characters: English alphabet letters, digits and whitespace"

    def __init__(self, name: str, day: int, hour: int, minute: int):
        self.name: str = name
        self.day: int = day
        self.hour: int = hour
        self.minute: int = minute

    def __str__(self):
        return f'"{self.name}", day {self.day} at {self.hour:02}:{self.minute:02}'

    def __repr__(self):
        return f'{self.name}@{self.day}.{self.hour:02}.{self.minute:02}'

    def __eq__(self, other):
        if not isinstance(other, SaveState):
            return False
        return self.name == other.name

    def get_time_str(self) -> str:
        """
        :return: a string with a description of the time of the save
        """
        return f'Day {self.day}, hour {self.hour}, min {self.minute}'

    @classmethod
    def is_name_valid(cls, name: str) -> bool:
        """
        :return True if the given name is valid, False otherwise
        """
        return re.match("^" + cls._NAME_PAT + "$", name) is not None

    @staticmethod
    def is_time_valid(day: int, hour: int, minute: int) -> bool:
        """
        :return True if the given time is valid, False otherwise
        """
        return 1 <= day <= 3 and 0 <= hour <= 23 and 0 <= minute <= 59

    @classmethod
    def from_str(cls, string: str) -> SaveState:
        """
        Converts back a repr(SaveState)
        :param string: string to convert
        :return: SaveState with the given name and time
        """
        if re.match(cls._PATTERN, string) is None:
            raise ValueError("Invalid value: " + string)
        name, time = string.split('@')
        day, hour, minute = time.split('.')
        return SaveState(name, int(day), int(hour), int(minute))
