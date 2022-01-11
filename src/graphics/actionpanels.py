from __future__ import annotations

import logging
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from typing import Tuple, List

from src import ini, saves, music
from src.graphics.buttons import Button, Switch
from src.graphics.interfaces import Panel, Tickable
from src.timer import Clock

BTN_SIZE = 24
SIDE_PAD = 16

LOG = logging.getLogger(__name__)


def create_nav_panel(root: tk.Tk, clock: Clock, parent: Panel, width: int, height: int) -> Panel:
    nav = ButtonPanel(clock)

    pause_btn = Switch(root, ini.img('run-off'), ini.img('run-on'), 'RUN',
                       [clock.un_pause], lambda: getattr(clock, "running"))
    # the action needs the button, a simple on/off doesn't work as clock.running is changed by a lot of other objects

    slow_btn = Switch(root, ini.img('slow-off'), ini.img('slow-on'), 'SLOWER',
                      [clock.cycle_millis], lambda: getattr(clock, "slow"))

    forward_btn = Button(root, ini.img('fwd'), 'FWD', [clock.forward, pause_btn.tick, slow_btn.tick, parent.tick])

    backward_btn = Button(root, ini.img('bwd'), 'BWD', [clock.backward, pause_btn.tick, slow_btn.tick, parent.tick])

    reset_btn = Button(root, ini.img('reset'), 'RESET', [clock.reset, pause_btn.tick, slow_btn.tick, parent.tick])

    nav.add_button(slow_btn, SIDE_PAD, height)
    nav.add_button(pause_btn, SIDE_PAD + BTN_SIZE + SIDE_PAD, height)

    nav.add_button(forward_btn, width - SIDE_PAD - BTN_SIZE, height)
    nav.add_button(backward_btn, width - 2 * SIDE_PAD - 2 * BTN_SIZE, height)
    nav.add_button(reset_btn, width - 2 * SIDE_PAD - 4 * BTN_SIZE, height)

    return nav


def create_save_panel(root: tk.Tk, clock: Clock, parent: Panel, width: int, height: int) -> Panel:
    return SavePanel(root, clock, parent, width, height)


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

    def __init__(self, root: tk.Tk, clock: Clock, parent: Panel, width: int, height: int):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.parent: Panel = parent
        self.width: int = width
        self.height: int = height
        self._save_btn: Button = Button(self.root, ini.img('save'), 'SAVE', [self._save])
        self._delete_btn: Button = Button(self.root, ini.img('delete'), 'DELETE', [self._delete])
        self._load_btn: Button = Button(self.root, ini.img('load'), 'LOAD', [self._load])
        self._save_input: ttk.Entry = ttk.Entry(self.root, width=self._ENTRY_WIDTH)

        self._menu: ttk.Combobox = ttk.Combobox(self.root,
                                                values=saves.get_list(),
                                                width=self._ENTRY_WIDTH,
                                                # postcommand runs upon drop down
                                                postcommand=self._update_saves)

    def draw(self) -> None:
        # from left to right: delete, load, drop-down list
        self._delete_btn.place(SIDE_PAD, self.height)
        self._load_btn.place(SIDE_PAD + BTN_SIZE, self.height)
        self._menu.place(x=SIDE_PAD + 2 * BTN_SIZE, y=self.height)
        # from right to left: save, input field
        self._save_btn.place(self.width - SIDE_PAD - BTN_SIZE, self.height)
        self._save_input.place(x=self.width - SIDE_PAD - BTN_SIZE - 6 * self._ENTRY_WIDTH - SIDE_PAD / 2, y=self.height)

    def tick(self) -> None:
        pass

    def _save(self) -> None:
        """ If the input name is valid, creates a new save with the given name and at the current time """
        self.clock.un_pause('stop')
        self.parent.tick()
        name = self._save_input.get().strip()
        LOG.debug('Trying to save with name "%s" at time %s', name, self.clock.get_time_str())
        try:
            save = saves.create(name, self.clock.day, self.clock.hour, self.clock.minute)
            LOG.info('Saved "%s"', repr(save))
            self._save_input.delete(0, len(self._save_input.get()))
        except ValueError as e:
            LOG.warning('Invalid save "%s": %s', name, str(e))
            tkinter.messagebox.showinfo(title='Save error', message=str(e) + f'\n{saves.NAME_RULES}')

    def _update_saves(self) -> None:
        """ Updates the list of savestates """
        self._menu['values'] = saves.get_list()

    def _load(self) -> None:
        """ Gives the choice to load the selected save, showing the save time. On load, the save is deleted """
        self._select_and_exec('Load save', 'Load the following save?', 'Loaded save "%s"', True)

    def _delete(self) -> None:
        """ Gives the choice to delete the selected save, showing the save time. """
        self._select_and_exec('Delete save', 'Delete the following save?', 'Deleted save "%s"', False)

    def _select_and_exec(self, title: str, msg: str, log_msg: str, is_load: bool) -> None:
        """
        If the name selected in the menu corresponds to a savestate, shows a pop-up with a choice (load/delete).

        :param title: pop-up title
        :param msg: pop-up message preceding the savestate's details
        :param log_msg: log message with a '%s' where the savestate is shown
        :param is_load: if True, moves the clock to the savestate's time
        """
        name = self._menu.get()
        save = saves.get(name)
        if save is None:
            return
        self.clock.un_pause('stop')
        choice = tkinter.messagebox.askokcancel(
            title=title,
            message=f'{msg}\n{save.name}\n{save.get_time_str()}')
        if choice:
            if is_load:
                self.clock.set_time(save.day, save.hour, save.minute)
            music.stop()
            saves.delete(name)
            LOG.info(log_msg, repr(save))
        self.parent.tick()
        self._menu.delete(0, len(name))
