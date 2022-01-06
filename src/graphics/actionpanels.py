from __future__ import annotations

import tkinter as tk
from typing import Tuple, List

from src import ini
from src.graphics.buttons import Button, Switch, ButtonAction
from src.graphics.panels import Panel
from src.timer import Clock

BTN_SIZE = 24
BTN_PADDING = 16


def create_nav_panel(root: tk.Tk, clock: Clock, parent: Panel, width: int, height: int) -> Panel:
    nav = ButtonPanel(clock)

    pause_btn = Switch(root, ini.img('run-off'), ini.img('run-on'), None)
    # the action needs the button, a simple on/off doesn't work as clock.running is changed by a lot of other objects
    pause_act = ButtonAction(clock, start=[clock.un_pause], middle=[(pause_btn.set_on, "running")])
    pause_btn.action = pause_act

    slow_btn = Switch(root, ini.img('slow-off'), ini.img('slow-on'), None)
    slow_act = ButtonAction(clock, start=[clock.cycle_millis], middle=[(slow_btn.set_on, "slow")])
    slow_btn.action = slow_act

    forward_act = ButtonAction(
        clock,
        start=[clock.forward],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    forward_btn = Button(root, ini.img('fwd'), forward_act)

    backward_act = ButtonAction(
        clock,
        start=[clock.backward],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    backward_btn = Button(root, ini.img('bwd'), backward_act)

    reset_act = ButtonAction(
        clock,
        start=[clock.reset],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    reset_btn = Button(root, ini.img('reset'), reset_act)

    nav.add_button(slow_btn, BTN_PADDING, height)
    nav.add_button(pause_btn, BTN_PADDING + BTN_SIZE + BTN_PADDING, height)

    nav.add_button(forward_btn, width - BTN_PADDING - BTN_SIZE, height)
    nav.add_button(backward_btn, width - 2 * BTN_PADDING - 2 * BTN_SIZE, height)
    nav.add_button(reset_btn, width - 2 * BTN_PADDING - 4 * BTN_SIZE, height)

    return nav


class ButtonPanel(Panel):
    """
    Represents a panel containing various buttons.
    """

    def __init__(self, clock: Clock):
        self.clock: Clock = clock
        self._buttons: List[Tuple[Button, int, int]] = []

    def draw(self) -> None:
        for btn, pos_x, pos_y in self._buttons:
            btn.place(pos_x, pos_y)

    def tick(self) -> None:
        """ Nothing to do """
        pass

    def add_button(self, btn: Button, pos_x: int, pos_y: int) -> None:
        """
        :param btn: button to add
        :param pos_x: button x-coordinate
        :param pos_y: button y-coordinate
        """
        self._buttons.append((btn, pos_x, pos_y))
