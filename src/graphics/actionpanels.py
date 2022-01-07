from __future__ import annotations

import re
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from typing import Tuple, List, Dict, Optional

from src import ini
from src.graphics.buttons import Button, Switch, ButtonAction
from src.graphics.interfaces import Panel, Tickable
from src.timer import Clock, ClockTime

BTN_SIZE = 24
SIDE_PAD = 16


def create_nav_panel(root: tk.Tk, clock: Clock, parent: Panel, width: int, height: int) -> Panel:
    nav = ButtonPanel(clock)

    pause_btn = Switch(root, ini.img('run-off'), ini.img('run-on'), None, lambda: getattr(clock, "running"))
    # the action needs the button, a simple on/off doesn't work as clock.running is changed by a lot of other objects
    pause_act = ButtonAction(clock, start=[clock.un_pause], middle=[pause_btn.tick])
    pause_btn.action = pause_act

    slow_btn = Switch(root, ini.img('slow-off'), ini.img('slow-on'), None, lambda: getattr(clock, "slow"))
    slow_act = ButtonAction(clock, start=[clock.cycle_millis], middle=[slow_btn.tick])
    slow_btn.action = slow_act

    forward_act = ButtonAction(
        clock,
        start=[clock.forward],
        middle=[pause_btn.tick, slow_btn.tick],
        end=[parent.tick])
    forward_btn = Button(root, ini.img('fwd'), forward_act)

    backward_act = ButtonAction(
        clock,
        start=[clock.backward],
        middle=[pause_btn.tick, slow_btn.tick],
        end=[parent.tick])
    backward_btn = Button(root, ini.img('bwd'), backward_act)

    reset_act = ButtonAction(
        clock,
        start=[clock.reset],
        middle=[pause_btn.tick, slow_btn.tick],
        end=[parent.tick])
    reset_btn = Button(root, ini.img('reset'), reset_act)

    nav.add_button(slow_btn, SIDE_PAD, height)
    nav.add_button(pause_btn, SIDE_PAD + BTN_SIZE + SIDE_PAD, height)

    nav.add_button(forward_btn, width - SIDE_PAD - BTN_SIZE, height)
    nav.add_button(backward_btn, width - 2 * SIDE_PAD - 2 * BTN_SIZE, height)
    nav.add_button(reset_btn, width - 2 * SIDE_PAD - 4 * BTN_SIZE, height)

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
        for btn, _, _ in self._buttons:
            if isinstance(btn, Tickable):
                btn.tick()

    def add_button(self, btn: Button, pos_x: int, pos_y: int) -> None:
        """
        :param btn: button to add
        :param pos_x: button x-coordinate
        :param pos_y: button y-coordinate
        """
        self._buttons.append((btn, pos_x, pos_y))


class SavePanel(Panel):
    _ENTRY_WIDTH = 16
    _ENTRY_PATTERN = "^[a-zA-Z0-9 ]{1,16}$"
    _ENTRY_RULES = "Rules:\n - length 1 to 16;\n - allowed characters: English alphabet letters, digits and whitespace"

    def __init__(self, root: tk.Tk, clock: Clock, width: int, height: int, parent: Panel):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.width: int = width
        self.height: int = height
        self.parent: Panel = parent
        self._save_btn: Button = Button(self.root, ini.img('reset'), self._save)
        self._load_btn: Button = Button(self.root, ini.img('reset'), self._load)
        self._save_input: ttk.Entry = ttk.Entry(self.root, width=self._ENTRY_WIDTH)

        self._saves: Dict[str, ClockTime] = {}
        self._menu: ttk.Combobox = ttk.Combobox(self.root,
                                                values=list(self._saves.keys()),
                                                width=self._ENTRY_WIDTH,
                                                # postcommand runs upon drop down
                                                postcommand=self._update_saves)

    def draw(self) -> None:
        """ On the left side, the list of files and the load button, on the right the input form and the save button """
        self._load_btn.place(SIDE_PAD, self.height)
        self._menu.place(x=SIDE_PAD + BTN_SIZE, y=self.height)
        self._save_btn.place(self.width - SIDE_PAD - BTN_SIZE, self.height)
        self._save_input.place(x=self.width - SIDE_PAD - BTN_SIZE - 6 * self._ENTRY_WIDTH - SIDE_PAD / 2, y=self.height)

    def tick(self) -> None:
        pass

    def _check_name(self, name: str) -> Optional[str]:
        """
        Checks whether the given string can be used as name for a save.
        It must match the defined pattern, and it must be unique.
        :param name: string to check
        :return: None if the string is valid, an error message otherwise
        """
        if re.match(self._ENTRY_PATTERN, name) is None:
            return f'"{name}" is invalid.\n{self._ENTRY_RULES}'
        if name in self._saves:
            return f'"{name}" already in use'
        return None

    def _save(self) -> None:
        """ If the input name is valid, creates a new save with the given name and at the current time """
        self.clock.un_pause('stop')
        name = self._save_input.get()
        err = self._check_name(name)
        if err is not None:  # err:=self._check_name(name) here?
            tkinter.messagebox.showinfo(title='Invalid name', message=err)
        else:
            self._saves[name] = ClockTime(self.clock.day, self.clock.hour, self.clock.minute)
            self._save_input.delete(0, len(self._save_input.get()))

    def _update_saves(self) -> None:
        """ Updates the list of savestates """
        self._menu['values'] = list(self._saves.keys())

    def _load(self) -> None:
        """ Gives the choice to load the selected save, showing the save time. On load, the save is deleted """
        name = self._menu.get()
        if not name:
            return
        value = self._saves[name]
        self.clock.un_pause('stop')
        choice = tkinter.messagebox.askokcancel(
            title='Confirm load',
            message=f'Load the following save?\n{name}\n{value}')
        if choice:
            self.clock.set_time(value)
            self._saves.pop(name, None)
            self.parent.tick()
        self._menu.delete(0, len(name))
