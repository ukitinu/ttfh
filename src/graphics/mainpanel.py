from __future__ import annotations

import tkinter as tk

from src import timer
from src.graphics.actionpanels import ButtonPanel
from src.graphics.panels import TextPanel, PanelStyle, ClockPanel, Panel
from src.timer import Clock


class MainPanel(Panel):
    _BG_COLOUR = '#000000'
    _DAY_HEIGHT = 64
    _PERIOD_HEIGHT = 32
    _BTN_HEIGHT = 48

    def __init__(self, root: tk.Tk, clock: Clock, width: int, height: int):
        self.root = root
        self.clock = clock
        self.width = width
        self.height = height
        self.hour_height = self.height - self._DAY_HEIGHT - self._PERIOD_HEIGHT - self._BTN_HEIGHT

        self.day_panel: Panel = TextPanel(self.root, self.clock,
                                          PanelStyle(self.width, self._DAY_HEIGHT, self._BG_COLOUR,
                                                     'Arial 24 bold'),
                                          timer.get_day)

        self.period_panel: Panel = TextPanel(self.root, self.clock,
                                             PanelStyle(self.width, self._PERIOD_HEIGHT, self._BG_COLOUR,
                                                        'Arial 18 bold'),
                                             timer.get_period)

        self.clock_panel: Panel = ClockPanel(self.root, self.clock,
                                             PanelStyle(self.width, self.hour_height, self._BG_COLOUR,
                                                        'Arial 64'),
                                             timer.get_time)

        self.button_panel: Panel = ButtonPanel(self.root, self.clock, self)

    def draw(self):
        self.day_panel.draw()
        self.period_panel.draw()
        self.clock_panel.draw()
        self.button_panel.draw()

    def tick(self):
        self.day_panel.tick()
        self.period_panel.tick()
        self.clock_panel.tick()
