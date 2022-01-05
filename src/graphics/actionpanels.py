from __future__ import annotations

import tkinter as tk

from src import ini
from src.graphics.button import Button
from src.graphics.panels import Panel
from src.graphics.switch import Switch
from src.timer import Clock


class ButtonPanel(Panel):
    """
    Represents a panel containing various buttons. Right now it is VERY concrete. If and when in the future more
    objects similar are required, it will be reworked.
    """

    def __init__(self, root: tk.Tk, clock: Clock, parent: Panel):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.parent: Panel = parent

        self.slow_btn: Switch = None
        self.pause_btn: Switch = None
        self.reset_btn: Button = None
        self.forward_btn: Button = None
        self.backward_btn: Button = None

    def draw(self) -> None:
        self.slow_btn = Switch(self.root, ini.get_img('slow-off'), ini.get_img('slow-on'), self.__slow)
        self.slow_btn.pack(side='left', padx=16, pady=10)
        self.pause_btn = Switch(self.root, ini.get_img('run-off'), ini.get_img('run-on'), self.__pause)
        self.pause_btn.pack(side='left', padx=16, pady=10)
        self.forward_btn = Button(self.root, ini.get_img('fwd'), self.__fwd).pack(side='right', padx=16, pady=10)
        self.backward_btn = Button(self.root, ini.get_img('bwd'), self.__bwd).pack(side='right', padx=0, pady=10)
        self.reset_btn = Button(self.root, ini.get_img('reset'), self.__reset).pack(side='right', padx=24, pady=10)

    def tick(self) -> None:
        pass

    def __slow(self) -> None:
        self.clock.cycle_millis()
        self.slow_btn.set_on(self.clock.slow)

    def __pause(self) -> None:
        self.clock.un_pause()
        self.pause_btn.set_on(self.clock.running)

    def __reset(self) -> None:
        self.clock.reset()
        self.pause_btn.set_on(self.clock.running)
        self.slow_btn.set_on(self.clock.slow)
        self.parent.tick()

    def __fwd(self) -> None:
        self.clock.forward()
        self.pause_btn.set_on(self.clock.running)
        self.slow_btn.set_on(self.clock.slow)
        self.parent.tick()

    def __bwd(self) -> None:
        self.clock.backward()
        self.pause_btn.set_on(self.clock.running)
        self.slow_btn.set_on(self.clock.slow)
        self.parent.tick()
