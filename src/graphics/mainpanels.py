from __future__ import annotations

import tkinter as tk
from operator import itemgetter
from typing import List, Tuple

from src import timer
from src.graphics import actionpanels
from src.graphics.panels import TextPanel, PanelStyle, ClockPanel, Panel
from src.timer import Clock

_BG_COLOUR = '#000000'
_DAY_HEIGHT = 64
_PERIOD_HEIGHT = 32
_BTN_HEIGHT = 48
_SAVE_HEIGHT = 40


def create_main_panel(root: tk.Tk, clock: Clock, width: int, height: int) -> Panel:
    """
    Creates the main panel of TTFH.

    :param root: tkinter element on which to put the panel
    :param clock: clock to display and control
    :param width: tkinter window width
    :param height: tkinter window height
    :return: main panel
    """
    main = PanelHolder(width, height)

    # from the top
    day = TextPanel(root, clock, PanelStyle(width, _DAY_HEIGHT, _BG_COLOUR, 'Arial 24 bold'), timer.get_day)
    period = TextPanel(root, clock, PanelStyle(width, _PERIOD_HEIGHT, _BG_COLOUR, 'Arial 18 bold'), timer.get_period)

    hour_height = height - _DAY_HEIGHT - _PERIOD_HEIGHT - _BTN_HEIGHT - _SAVE_HEIGHT
    hour = ClockPanel(root, clock, PanelStyle(width, hour_height, _BG_COLOUR, 'Arial 64'), timer.get_time)

    # from the bottom
    saves = actionpanels.SavePanel(root, clock, width, height - _SAVE_HEIGHT)
    buttons = actionpanels.create_nav_panel(root, clock, main, width, height - _SAVE_HEIGHT - _BTN_HEIGHT)

    main.add_panel(day, 1, True)
    main.add_panel(period, 2, True)
    main.add_panel(hour, 3, True)
    main.add_panel(buttons, 4, False)
    main.add_panel(saves, 5, False)

    return main


class PanelHolder(Panel):
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self._panels: List[Tuple[int, Panel, bool]] = []

    def draw(self) -> None:
        self._panels.sort(key=itemgetter(0))
        for _, panel, _ in self._panels:
            panel.draw()

    def tick(self) -> None:
        self._panels.sort(key=itemgetter(0))
        for _, panel, do_tick in self._panels:
            if do_tick:
                panel.tick()

    def add_panel(self, panel: Panel, order: int, do_tick: bool = False) -> None:
        """
        :param panel: panel to add
        :param order: integer representing the draw (and tick) order of the panel
        :param do_tick: if true, the method tick() will be called on the panel
        """
        self._panels.append((order, panel, do_tick))
