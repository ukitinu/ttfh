import tkinter as tk
from typing import Callable


class SwitchStyle:
    __RELIEF_ON = tk.SUNKEN
    __RELIEF_OFF = tk.RAISED
    __COLOUR_ON = '#aaaaaa'
    __COLOUR_OFF = 'white'

    def __init__(self, master: tk, ):
        self.var = tk.StringVar(master, f'{self.__RELIEF_OFF}:{self.__COLOUR_OFF}')

    def switch(self, active: bool):
        relief = self.__RELIEF_ON if active else self.__RELIEF_OFF
        colour = self.__COLOUR_ON if active else self.__COLOUR_OFF
        self.var.set(f'{relief}:{colour}')

    def get(self):
        return self.var.get()

    def set(self, value: str):
        return self.var.set(value)

    def trace_add(self, callback: Callable):
        self.var.trace_add('write', callback)
