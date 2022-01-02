from __future__ import annotations

import tkinter as tk
from typing import Callable

from src.graphics.panel import Panel
from src.timer import Clock


class TextPanelStyle:
    """ This class holds the immutable style properties of the TextPanel """

    def __init__(self, width: int, height: int, bg_colour: str, font: str):
        self.width: int = width
        self.height: int = height
        self.bg_colour: str = bg_colour
        self.font: str = font


class TextPanel(Panel):
    """
    Represents a canvas containing one or more texts with, possibly, some variable styles and content.
    """

    def __init__(self, root: tk.Tk, clock: Clock, style: TextPanelStyle, var_callback: Callable[[Clock], str]):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.style: TextPanelStyle = style
        self.var_callback: Callable = var_callback
        self.style_var = tk.StringVar(self.root, self.var_callback(self.clock))

    def draw(self) -> None:
        canvas = tk.Canvas(self.root, width=self.style.width, height=self.style.height,
                           bg=self.style.bg_colour, highlightthickness=0)
        text_id = canvas.create_text(self.style.width / 2, self.style.height / 2,
                                     anchor=tk.CENTER,
                                     text=self.style_var.get().split(":")[0],
                                     fill=self.style_var.get().split(":")[1],
                                     font=self.style.font)
        canvas.pack()

        def on_change(varname, index, mode):
            """ The signature of the method must stay as is to work properly with tkinter """
            canvas.itemconfigure(text_id,
                                 text=self.style_var.get().split(":")[0],
                                 fill=self.style_var.get().split(":")[1])

        self.style_var.trace_add('write', on_change)

    def tick(self) -> None:
        self.style_var.set(self.var_callback(self.clock))
