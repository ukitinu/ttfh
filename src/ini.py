import configparser
from errno import ENOENT
import os

from definitions import INI_FILE

if not os.path.exists(INI_FILE):
    raise FileNotFoundError(ENOENT, os.strerror(ENOENT), INI_FILE)

ini_values = configparser.ConfigParser()
ini_values.read(INI_FILE)


def get_label(key: str) -> str:
    return __get('LABELS', key)


def get_timer(key: str) -> str:
    return __get('TIMER', key)


def get_sound(key: str) -> str:
    return __get('SOUNDS', key)


def get_sys(key: str) -> str:
    return __get('SYSTEM', key)


def __get(section: str, key: str) -> str:
    return ini_values[section][key]
