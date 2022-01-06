from __future__ import annotations

import tkinter as tk
from typing import Callable, List, Tuple

from src.timer import Clock


class ButtonAction:
    def __init__(self,
                 clock: Clock,
                 start: List[Callable] = None,
                 middle: List[Tuple[Callable, str]] = None,
                 end: List[Callable] = None):
        """
        :param start: callables to execute first
        :param middle: callables and switch's set_on to execute in-between. If the str is None the callable
        is executed without argument, otherwise it is executed with getattr(self.clock, str)
        :param end: callables to execute last
        """
        if start is None:
            start = []
        if middle is None:
            middle = []
        if end is None:
            end = []
        self.clock: Clock = clock
        self.start: List[Callable] = start
        self.middle: List[Tuple[Callable, str]] = middle
        self.end: List[Callable] = end

    def exec(self) -> None:
        """ Executes the button action """
        for cmd in self.start:
            cmd()
        for cmd, attr in self.middle:
            if attr is not None:
                val = getattr(self.clock, attr)
                cmd(val)
            else:
                cmd()
        for cmd in self.end:
            cmd()


class Button:
    _RELIEF = tk.GROOVE

    def __init__(self, root: tk.Tk, icon_path: str, action: ButtonAction, **kwargs):
        """
        :param root: root Tk of the button
        :param icon_path: path to the PNG icon
        :param action: action to call on click
        :param kwargs: additional arguments for the button's creation
        """
        self.root: tk.Tk = root
        self.icon: tk.PhotoImage = tk.PhotoImage(file=icon_path)
        self.action: ButtonAction = action
        self.style_args = kwargs
        self._btn: tk.Button = None

    def place(self, pos_x: int, pos_y: int) -> Button:
        """
        Packs the button. If no 'relief' argument was given at instantiation, it uses tk.GROOVE.
        :param pos_x: x-coordinate of the button
        :param pos_y: y-coordinate of the button
        :return: the object itself
        """
        if 'relief' not in self.style_args:
            self.style_args['relief'] = self._RELIEF

        self._btn = tk.Button(self.root, image=self.icon, command=self.action.exec, **self.style_args)
        self._btn.place(x=pos_x, y=pos_y)
        return self


class Switch(Button):
    _RELIEF_ON = tk.SUNKEN
    _RELIEF_OFF = tk.RAISED

    def __init__(self, root: tk.Tk, icon_off: str, icon_on: str, action: ButtonAction, **kwargs):
        """
        Creates a switch, a button with two states, represented by two different values of the 'relief' property and
        two different icons.

        :param root: root Tk of the switch
        :param icon_off: path to the PNG icon used when the button is off
        :param icon_on: path to the PNG icon used when the button is on
        :param action: action to call on click
        :param kwargs: additional arguments for the button's creation
        """
        super().__init__(root, icon_off, action, relief=self._RELIEF_OFF, **kwargs)
        self.icon_on: tk.PhotoImage = tk.PhotoImage(file=icon_on)
        self.var: tk.BooleanVar = tk.BooleanVar(root, False)

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

    def set_on(self, active: bool) -> None:
        """
        Sets the switch's status, True on, False off.

        :param active: bool of the new status of the switch.
        """
        self.var.set(active)
