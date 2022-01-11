from __future__ import annotations

import logging
import tkinter as tk
from typing import Callable, List

from src.graphics.interfaces import Tickable

LOG = logging.getLogger(__name__)


class ButtonAction:
    def __init__(self, callables: List[Callable]):
        """
        :param callables: ordered callables
        """
        self.callables: List[Callable] = callables

    def exec(self) -> None:
        """ Executes the button action """
        for cmd in self.callables:
            cmd()


class Button:
    _RELIEF = tk.GROOVE

    def __init__(self, root: tk.Tk, icon_path: str, name: str, action: List[Callable], **kwargs):
        """
        :param root: root Tk of the button
        :param icon_path: path to the PNG icon
        :param name: button name
        :param action: ordered list of callables to call on click
        :param kwargs: additional arguments for the button's creation
        """
        action.append(lambda: LOG.info('Clicked on %s', str(self)))

        self.root: tk.Tk = root
        self.name: str = name
        self.icon: tk.PhotoImage = tk.PhotoImage(file=icon_path)
        self.action: ButtonAction = ButtonAction(action)
        self.style_args = kwargs
        self._btn: tk.Button = None

    def __str__(self):
        """ Uses the name to identify the button, override as needed. """
        return f'button::{self.name}'

    def place(self, pos_x: int, pos_y: int) -> Button:
        """
        Packs the button. If no 'relief' argument was given at instantiation, it uses tk.GROOVE.
        :param pos_x: x-coordinate of the button
        :param pos_y: y-coordinate of the button
        :return: the object itself
        """
        if 'relief' not in self.style_args:
            self.style_args['relief'] = self._RELIEF

        self._btn = tk.Button(self.root,
                              image=self.icon,
                              command=self.action.exec,
                              **self.style_args)
        self._btn.place(x=pos_x, y=pos_y)
        return self


class Switch(Button, Tickable):
    _RELIEF_ON = tk.SUNKEN
    _RELIEF_OFF = tk.RAISED

    def __init__(self,
                 root: tk.Tk,
                 icon_off: str,
                 icon_on: str,
                 name: str,
                 action: List[Callable],
                 track: Callable[[], bool],
                 **kwargs):
        """
        Creates a switch, a button with two states, represented by two different values of the 'relief' property and
        two different icons.
        Appends self.tick to the list of callables.

        :param root: root Tk of the switch
        :param icon_off: path to the PNG icon used when the button is off
        :param icon_on: path to the PNG icon used when the button is on
        :param name: switch name
        :param action: ordered list of callables to call on click
        :param track: function returning a truthy value that tracks the switch's activation state
        :param kwargs: additional arguments for the button's creation
        """
        action.append(self.tick)
        super().__init__(root, icon_off, name, action, relief=self._RELIEF_OFF, **kwargs)
        self.icon_on: tk.PhotoImage = tk.PhotoImage(file=icon_on)
        self.track: Callable[[], bool] = track
        self.var: tk.BooleanVar = tk.BooleanVar(root, self.track())

    def __str__(self):
        """ Logs both id and state """
        return f'switch::{self.name}::' + ('ON' if self.var.get() else 'OFF')

    def place(self, pos_x: int, pos_y: int) -> Switch:
        """
        Packs the switch and updates its appearance based on self.var value.
        The unused variables in the 'on_change' function are required by Tk.

        :param pos_x: x-coordinate of the button
        :param pos_y: y-coordinate of the button
        :return: the object itself
        """
        super().place(pos_x, pos_y)

        def on_change(varname, index, mode):
            """ self.icon is icon_off """
            relief = self._RELIEF_ON if self.var.get() else self._RELIEF_OFF
            icon_img = self.icon_on if self.var.get() else self.icon
            self._btn.configure(relief=relief, image=icon_img)

        self.var.trace_add('write', on_change)

        return self

    def tick(self) -> None:
        self.var.set(self.track())
