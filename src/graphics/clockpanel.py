from __future__ import annotations

import tkinter as tk

from src import ini
from src import timer
from src.graphics.button import Button
from src.graphics.switch import Switch
from src.graphics.textpanel import TextPanel, TextPanelStyle
from src.timer import Clock

_BG_COLOUR = '#000000'

_DAY_HEIGHT = 64
_PERIOD_HEIGHT = 32
_BTN_HEIGHT = 48
_HOUR_HEIGHT = _HEIGHT - _DAY_HEIGHT - _PERIOD_HEIGHT - _BTN_HEIGHT


class ClockPanel:

    def __init__(self, root: tk.Tk, clock: Clock, width: int, height: int):
        self.root = root
        self.clock = clock
        self.width = width
        self.height = height

        self.day_panel: TextPanel = TextPanel(self.root, self.clock,
                                              TextPanelStyle(self.width, _DAY_HEIGHT, _BG_COLOUR, 'Arial 24 bold'),
                                              timer.get_day)

        self.period_panel: TextPanel = TextPanel(self.root, self.clock,
                                                 TextPanelStyle(self.width, _PERIOD_HEIGHT, _BG_COLOUR,
                                                                'Arial 18 bold'),
                                                 timer.get_period)

        self.time = tk.StringVar(self.root, timer.get_time(self.clock))

        self.slow_btn: Switch = None
        self.pause_btn: Switch = None
        self.reset_btn: Button = None
        self.forward_btn: Button = None
        self.backward_btn: Button = None

    def draw(self):
        self.day_panel.draw()
        self.period_panel.draw()
        self.__draw_hour_canvas()
        self.__draw_buttons()

    def tick(self):
        self.day_panel.tick()
        self.period_panel.tick()
        self.time.set(timer.get_time(self.clock))

    def __draw_buttons(self) -> None:
        self.slow_btn = Switch(self.root, ini.get_img('slow-off'), ini.get_img('slow-on'), self.__slow)
        self.slow_btn.pack(side='left', padx=16, pady=10)
        self.pause_btn = Switch(self.root, ini.get_img('run-off'), ini.get_img('run-on'), self.__pause)
        self.pause_btn.pack(side='left', padx=16, pady=10)
        self.forward_btn = Button(self.root, ini.get_img('fwd'), self.__fwd).pack(side='right', padx=16, pady=10)
        self.backward_btn = Button(self.root, ini.get_img('bwd'), self.__bwd).pack(side='right', padx=0, pady=10)
        self.reset_btn = Button(self.root, ini.get_img('reset'), self.__reset).pack(side='right', padx=24, pady=10)

    def __draw_hour_canvas(self) -> None:
        hour_canvas = tk.Canvas(self.root, width=self.width, height=self.__HOUR_HEIGHT, bg=_BG_COLOUR,
                                highlightthickness=0)
        text_id = hour_canvas.create_text(self.width / 2, self.__HOUR_HEIGHT / 2,
                                          text=self.time.get().split(":")[0],
                                          fill='white',
                                          font='Arial 64')
        self.__draw_circle(hour_canvas, self.width // 2, self.__HOUR_HEIGHT // 2, self.width // 3,
                           outline='white',
                           width=8)
        arc_id = self.__draw_circle(hour_canvas, self.width // 2, self.__HOUR_HEIGHT // 2, self.width // 3,
                                    outline='red',
                                    width=6,
                                    extent=-1 * int(self.time.get().split(":")[1]) * 6)
        hour_canvas.pack()

        def on_change(varname, index, mode):
            hour = self.root.getvar(varname).split(":")[0]
            hour_canvas.itemconfigure(text_id, text=hour)

            minutes = int(self.root.getvar(varname).split(":")[1])
            extent = self.__calc_arc_extent(minutes)
            hour_canvas.itemconfigure(arc_id, extent=extent)

        self.time.trace_add('write', on_change)
