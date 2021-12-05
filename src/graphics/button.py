from __future__ import annotations
import tkinter as tk
from typing import Callable


class Button:
    __RELIEF = tk.GROOVE

    def __init__(self, master: tk.Tk, icon_path: str, cmd: Callable, **kwargs):
        """
        :param master: parent of the button
        :param icon_path: path to the PNG icon
        :param cmd: function to call on click
        :param kwargs: additional arguments for the button's creation
        """
        self.master: tk.Tk = master
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
            self.style_args['relief'] = self.__RELIEF

        self._btn = tk.Button(self.master, image=self.icon, command=self.cmd, **self.style_args)
        self._btn.pack(**kwargs)
        return self
