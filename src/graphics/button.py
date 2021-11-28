from __future__ import annotations
import tkinter as tk
from typing import Callable


class Button:

    def __init__(self, master: tk.Tk, bitmap: str, cmd: Callable = None, **kwargs):
        self.master: tk.Tk = master
        self.bitmap: str = bitmap
        self.photo = tk.PhotoImage(file='resources/images/reset.png')
        self.img_label = tk.Label(image=self.photo)
        self.cmd: Callable = cmd
        self.style_args = kwargs
        self._btn: tk.Button = None

    def pack(self, **kwargs) -> Button:
        self._btn = tk.Button(self.master, image=self.photo, command=self.cmd, **self.style_args)
        self._btn.pack(**kwargs)
        return self
