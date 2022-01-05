from __future__ import annotations

import tkinter as tk

from src import ini
from src import timer
from src.graphics.button import Button
from src.graphics.panels import TextPanel, PanelStyle, ClockPanel
from src.graphics.switch import Switch
from src.timer import Clock


class MainPanel:
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

        self.day_panel: TextPanel = TextPanel(self.root, self.clock,
                                              PanelStyle(self.width, self._DAY_HEIGHT, self._BG_COLOUR,
                                                         'Arial 24 bold'),
                                              timer.get_day)

        self.period_panel: TextPanel = TextPanel(self.root, self.clock,
                                                 PanelStyle(self.width, self._PERIOD_HEIGHT, self._BG_COLOUR,
                                                            'Arial 18 bold'),
                                                 timer.get_period)

        self.clock_panel: ClockPanel = ClockPanel(self.root, self.clock,
                                                  PanelStyle(self.width, self.hour_height, self._BG_COLOUR,
                                                             'Arial 64'),
                                                  timer.get_time)
        self.slow_btn: Switch = None
        self.pause_btn: Switch = None
        self.reset_btn: Button = None
        self.forward_btn: Button = None
        self.backward_btn: Button = None

    def draw(self):
        self.day_panel.draw()
        self.period_panel.draw()
        self.clock_panel.draw()
        # self.__draw_buttons()

    def tick(self):
        self.day_panel.tick()
        self.period_panel.tick()
        self.clock_panel.tick()

    # def __draw_buttons(self) -> None:
    #     self.slow_btn = Switch(self.root, ini.get_img('slow-off'), ini.get_img('slow-on'), self.__slow)
    #     self.slow_btn.pack(side='left', padx=16, pady=10)
    #     self.pause_btn = Switch(self.root, ini.get_img('run-off'), ini.get_img('run-on'), self.__pause)
    #     self.pause_btn.pack(side='left', padx=16, pady=10)
    #     self.forward_btn = Button(self.root, ini.get_img('fwd'), self.__fwd).pack(side='right', padx=16, pady=10)
    #     self.backward_btn = Button(self.root, ini.get_img('bwd'), self.__bwd).pack(side='right', padx=0, pady=10)
    #     self.reset_btn = Button(self.root, ini.get_img('reset'), self.__reset).pack(side='right', padx=24, pady=10)
