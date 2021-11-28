import os

from src import ini

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # https://github.com/pygame/pygame/issues/1468

from pygame import mixer

mixer.init()
__CHANNEL_CLOCK = 0
__CHANNEL_ENV = 1
__CHANNELS = [__CHANNEL_CLOCK, __CHANNEL_ENV]


def bells():
    __play('bells', __CHANNEL_CLOCK)


def tick():
    __play('tick', __CHANNEL_CLOCK)


def rumble():
    __play('rumble', __CHANNEL_ENV)


def new_day():
    __play('transition', __CHANNEL_CLOCK)


def stop():
    for channel in __CHANNELS:
        mixer.Channel(channel).stop()


def __play(key: str, channel: int):
    try:
        mixer.Channel(channel).play(mixer.Sound(ini.get_sound(key)))
    except FileNotFoundError:
        pass
