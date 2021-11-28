import os

from src import ini

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # https://github.com/pygame/pygame/issues/1468

from pygame import mixer

mixer.init()
__CHANNEL_CLOCK = 0
__CHANNEL_ENV = 1
__CHANNELS = [__CHANNEL_CLOCK, __CHANNEL_ENV]


def bells() -> None:
    """ Plays the bells. """
    __play('bells', __CHANNEL_CLOCK)


def tick() -> None:
    """ Plays a single clock tick. """
    __play('tick', __CHANNEL_CLOCK)


def rumble() -> None:
    """ Plays a low rumbling sound, tremors. On a different channel to allow its execution together with others. """
    __play('rumble', __CHANNEL_ENV)


def new_day() -> None:
    """ Plays a sound that remarks the start of a new day. """
    __play('transition', __CHANNEL_CLOCK)


def stop() -> None:
    """ Stops every sound immediately. """
    for channel in __CHANNELS:
        mixer.Channel(channel).stop()


def __play(key: str, channel: int) -> None:
    """
    Plays the sound at the specified path on the specified channel.
    If no file is found it does nothing.

    :param key: path to the sound file.
    :param channel: channel number, to allow multiple sounds simultaneously.
    """
    try:
        mixer.Channel(channel).play(mixer.Sound(ini.get_sound(key)))
    except FileNotFoundError:
        pass
