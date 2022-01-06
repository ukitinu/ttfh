import configparser
from errno import ENOENT
import os

from definitions import INI_FILE

if not os.path.exists(INI_FILE):
    raise FileNotFoundError(ENOENT, os.strerror(ENOENT), INI_FILE)

ini_values = configparser.ConfigParser()
ini_values.read(INI_FILE)


def gui(key: str) -> str:
    """ Gets GUI.key value from the .ini file """
    return __get('GUI', key)


def timer(key: str) -> str:
    """ Gets TIMER.key value from the .ini file """
    return __get('TIMER', key)


def sound(key: str) -> str:
    """ Gets SOUNDS.key value from the .ini file """
    return __get('SOUNDS', key)


def sys(key: str) -> str:
    """ Gets SYSTEM.key value from the .ini file """
    return __get('SYSTEM', key)


def img(key: str) -> str:
    """ Gets IMAGES.key value from the .ini file """
    return __get('IMAGES', key)


def __get(section: str, key: str) -> str:
    return ini_values[section][key]
