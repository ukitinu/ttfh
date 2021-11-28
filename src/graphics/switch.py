from __future__ import annotations
import tkinter as tk
from typing import Callable

from src.graphics.button import Button


class Switch(Button):
    __RELIEF_ON = tk.SUNKEN
    __RELIEF_OFF = tk.RAISED
    __COLOUR_ON = '#aaaaaa'
    __COLOUR_OFF = 'white'

    def __init__(self, master: tk.Tk, bitmap: str, cmd: Callable):
        super().__init__(master, bitmap, cmd, relief=self.__RELIEF_OFF, bg=self.__COLOUR_OFF)
        self.var: tk.StringVar = tk.StringVar(master, f'{self.__RELIEF_OFF}:{self.__COLOUR_OFF}')

    def pack(self, **kwargs) -> Switch:
        super().pack(**kwargs)

        def on_change(varname, index, mode):
            relief = self.master.getvar(varname).split(":")[0]
            bg = self.master.getvar(varname).split(":")[1]
            self._btn.configure(relief=relief, bg=bg)

        self.var.trace_add('write', on_change)

        return self

    def set_on(self, active: bool):
        relief = self.__RELIEF_ON if active else self.__RELIEF_OFF
        colour = self.__COLOUR_ON if active else self.__COLOUR_OFF
        self.var.set(f'{relief}:{colour}')
