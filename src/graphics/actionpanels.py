from __future__ import annotations

import tkinter as tk
from operator import itemgetter
from typing import Tuple, List

from src import ini
from src.graphics.buttons import Button, Switch, ButtonPosition, ButtonAction
from src.graphics.panels import Panel
from src.timer import Clock


def create_nav_panel(root: tk.Tk, clock: Clock, parent: Panel) -> Panel:
    nav = ButtonPanel(clock, parent)

    pause_pos = ButtonPosition('left', 16, 10)
    pause_btn = Switch(root, ini.get_img('run-off'), ini.get_img('run-on'), None)
    # the action needs the button, a simple on/off doesn't work as clock.running is changed by a lot of other objects
    pause_act = ButtonAction(clock, start=[clock.un_pause], middle=[(pause_btn.set_on, "running")])
    pause_btn.action = pause_act

    slow_pos = ButtonPosition('left', 16, 10)
    slow_btn = Switch(root, ini.get_img('slow-off'), ini.get_img('slow-on'), None)
    slow_act = ButtonAction(clock, start=[clock.cycle_millis], middle=[(slow_btn.set_on, "slow")])
    slow_btn.action = slow_act

    forward_pos = ButtonPosition('right', 16, 10)
    forward_act = ButtonAction(
        clock,
        start=[clock.forward],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    forward_btn = Button(root, ini.get_img('fwd'), forward_act)

    backward_pos = ButtonPosition('right', 0, 10)
    backward_act = ButtonAction(
        clock,
        start=[clock.backward],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    backward_btn = Button(root, ini.get_img('bwd'), backward_act)

    reset_pos = ButtonPosition('right', 24, 10)
    reset_act = ButtonAction(
        clock,
        start=[clock.reset],
        middle=[(pause_btn.set_on, "running"), (slow_btn.set_on, "slow")],
        end=[parent.tick])
    reset_btn = Button(root, ini.get_img('reset'), reset_act)

    nav.add_button(slow_btn, 1, slow_pos)
    nav.add_button(pause_btn, 2, pause_pos)
    nav.add_button(forward_btn, 3, forward_pos)
    nav.add_button(backward_btn, 4, backward_pos)
    nav.add_button(reset_btn, 5, reset_pos)

    return nav


class ButtonPanel(Panel):
    """
    Represents a panel containing various buttons.
    """

    def __init__(self, clock: Clock, parent: Panel):
        self.parent: Panel = parent
        self.clock: Clock = clock
        self.buttons: List[Tuple[int, Button, ButtonPosition]] = []

    def draw(self) -> None:
        self.buttons.sort(key=itemgetter(0))
        for _, btn, pos in self.buttons:
            btn.pack(pos)

    def tick(self) -> None:
        """ Nothing to do """
        pass

    def add_button(self, btn: Button, order: int, pos: ButtonPosition) -> None:
        """
        :param btn: button to add
        :param order: integer representing the draw order of the button
        :param pos: button position
        """
        self.buttons.append((order, btn, pos))
