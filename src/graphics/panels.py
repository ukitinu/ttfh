from __future__ import annotations

import tkinter as tk
from typing import Callable

from src.graphics import utils
from src.timer import Clock


class Panel:
    """ Interface for objects that can be drawn on the window """

    def draw(self) -> None:
        """ Draws the panel """
        pass

    def tick(self) -> None:
        """ Updates the panel """
        pass


class PanelStyle:
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

    def __init__(self, root: tk.Tk, clock: Clock, style: PanelStyle, var_callback: Callable[[Clock], str]):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.style: PanelStyle = style
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
            """
            The signature of the method must stay as is to work properly with tkinter.
            It also seems I can't move it from here to a more sensible place.
            """
            canvas.itemconfigure(text_id,
                                 text=self.style_var.get().split(":")[0],
                                 fill=self.style_var.get().split(":")[1])

        self.style_var.trace_add('write', on_change)

    def tick(self) -> None:
        self.style_var.set(self.var_callback(self.clock))


class ClockPanel(Panel):
    """
    Represents the canvas containing the clock with the hours and the circle.
    """

    def __init__(self, root: tk.Tk, clock: Clock, style: PanelStyle, var_callback: Callable[[Clock], str]):
        self.root: tk.Tk = root
        self.clock: Clock = clock
        self.style: PanelStyle = style
        self.var_callback: Callable = var_callback
        self.style_var = tk.StringVar(self.root, self.var_callback(self.clock))

    def draw(self) -> None:
        canvas = tk.Canvas(self.root, width=self.style.width, height=self.style.height,
                           bg=self.style.bg_colour, highlightthickness=0)
        text_id = canvas.create_text(self.style.width / 2, self.style.height / 2,
                                     anchor=tk.CENTER,
                                     text=self.style_var.get().split(":")[0],
                                     fill=self.style_var.get().split(":")[1],  # 'white'
                                     font=self.style.font)

        utils.draw_circle(canvas, self.style.width // 2, self.style.height // 2, self.style.width // 3,
                          outline='white',
                          width=8)

        arc_id = utils.draw_circle(canvas, self.style.width // 2, self.style.height // 2, self.style.width // 3,
                                   outline='red',
                                   width=6,
                                   extent=-1 * int(self.style_var.get().split(":")[1]) * 6)

        canvas.pack()

        def on_change(varname, index, mode):
            """
            The signature of the method must stay as is to work properly with tkinter.
            It also seems I can't move it from here to a more sensible place.
            """
            hour = self.style_var.get().split(":")[0]
            canvas.itemconfigure(text_id, text=hour)

            minutes = int(self.style_var.get().split(":")[1])
            extent = utils.calc_arc_extent(self.clock.day, self.clock.hour, minutes)
            canvas.itemconfigure(arc_id, extent=extent)

        self.style_var.trace_add('write', on_change)

    def tick(self) -> None:
        self.style_var.set(self.var_callback(self.clock))
