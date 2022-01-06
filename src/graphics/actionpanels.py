from __future__ import annotations

import tkinter as tk
from typing import Tuple, List

from src import ini
from src.graphics.buttons import Button, Switch, ButtonPosition
from src.graphics.panels import Panel
from src.timer import Clock


def create_nav_panel(root: tk.Tk, clock: Clock, parent: Panel) -> Panel:
    nav = ButtonPanel(clock, parent)

    # add order is important, defines display order
    slow_btn = Switch(root, ini.get_img('slow-off'), ini.get_img('slow-on'), self.__slow)
    slow_pos = ButtonPosition('left', 16, 10)

    pause_btn = Switch(root, ini.get_img('run-off'), ini.get_img('run-on'), self.__pause)
    pause_pos = ButtonPosition('left', 16, 10)

    forward_btn = Button(root, ini.get_img('fwd'), self.__fwd)
    forward_pos = ButtonPosition('right', 16, 10)

    backward_btn = Button(root, ini.get_img('bwd'), self.__bwd)
    backward_pos = ButtonPosition('right', 0, 10)

    reset_btn = Button(root, ini.get_img('reset'), self.__reset)
    reset_pos = ButtonPosition('right', 24, 10)



    return nav



class ButtonPanel(Panel):
    """
    Represents a panel containing various buttons.
    """

    def __init__(self, clock: Clock, parent: Panel):
        self.parent: Panel = parent
        self.clock: Clock = clock
        self.buttons: List[Tuple[Button, ButtonPosition]] = []

    def draw(self) -> None:
        for btn, pos in self.buttons:
            btn.pack(pos)

    def tick(self) -> None:
        pass

    def add_button(self, btn: Button, pos: ButtonPosition):
        self.buttons.append((btn, pos))

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
