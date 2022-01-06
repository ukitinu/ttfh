from __future__ import annotations

import tkinter as tk
from typing import Callable


class Button:
    _RELIEF = tk.GROOVE

    def __init__(self, parent: tk.Tk, icon_path: str, cmd: Callable, **kwargs):
        """
        :param parent: parent of the button
        :param icon_path: path to the PNG icon
        :param cmd: function to call on click
        :param kwargs: additional arguments for the button's creation
        """
        self.parent: tk.Tk = parent
        self.icon: tk.PhotoImage = tk.PhotoImage(file=icon_path)
        self.cmd: Callable = cmd
        self.style_args = kwargs
        self._btn: tk.Button = None

    def pack(self, **kwargs) -> Button:
        """
        Packs the button. If no 'relief' argument was given at instantiation, it uses tk.GROOVE.
        :param kwargs: additional arguments for the tk.Button.pack() function
        :return: the object itself
        """
        if 'relief' not in self.style_args:
            self.style_args['relief'] = self._RELIEF

        self._btn = tk.Button(self.parent, image=self.icon, command=self.cmd, **self.style_args)
        self._btn.pack(**kwargs)
        return self


class Switch(Button):
    _RELIEF_ON = tk.SUNKEN
    _RELIEF_OFF = tk.RAISED

    def __init__(self, master: tk.Tk, icon_off: str, icon_on: str, cmd: Callable, **kwargs):
        """
        Creates a switch, a button with two states, represented by two different values of the 'relief' property and
        two different icons.

        :param master: parent of the switch
        :param icon_off: path to the PNG icon used when the button is off
        :param icon_on: path to the PNG icon used when the button is on
        :param cmd: function to call on click
        :param kwargs: additional arguments for the button's creation
        """
        super().__init__(master, icon_off, cmd, relief=self._RELIEF_OFF, **kwargs)
        self.icon_on: tk.PhotoImage = tk.PhotoImage(file=icon_on)
        self.var: tk.StringVar = tk.StringVar(master, self._RELIEF_OFF)

    def pack(self, **kwargs) -> Switch:
        """
        Packs the switch and updates its appearance based on self.var value.
        The unused variables in the 'on_change' function are required by Tk.

        :param kwargs: additional arguments for the tk.Button.pack() function
        :return: the object itself
        """
        super().pack(**kwargs)

        def on_change(varname, index, mode):
            relief = self.parent.getvar(varname).split(":")[0]
            icon_img = self.icon if relief == tk.RAISED else self.icon_on
            self._btn.configure(relief=relief, image=icon_img)

        self.var.trace_add('write', on_change)

        return self

    def set_on(self, active: bool) -> None:
        """
        Sets the switch's status, True on, False off.

        :param active: bool of the new status of the switch.
        """
        relief = self._RELIEF_ON if active else self._RELIEF_OFF
        self.var.set(relief)
