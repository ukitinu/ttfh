from __future__ import annotations

import tkinter as tk
from typing import List

from src import timer
from src.graphics.actionpanels import ButtonPanel
from src.graphics.panels import TextPanel, PanelStyle, ClockPanel, Panel
from src.timer import Clock

_BG_COLOUR = '#000000'
_DAY_HEIGHT = 64
_PERIOD_HEIGHT = 32
_BTN_HEIGHT = 48


def create_main_panel(root: tk.Tk, clock: Clock, width: int, height: int) -> Panel:
    main = PanelHolder(root, width, height)
    main.add_display(TextPanel(root, clock, PanelStyle(width, _DAY_HEIGHT, _BG_COLOUR, 'Arial 24 bold'), timer.get_day))
    main.add_display(
        TextPanel(root, clock, PanelStyle(width, _PERIOD_HEIGHT, _BG_COLOUR, 'Arial 18 bold'), timer.get_period))

    hour_height = height - _DAY_HEIGHT - _PERIOD_HEIGHT - _BTN_HEIGHT
    main.add_display(ClockPanel(root, clock, PanelStyle(width, hour_height, _BG_COLOUR, 'Arial 64'), timer.get_time))

    main.add_action(ButtonPanel(root, clock, main))

    return main


class PanelHolder(Panel):
    def __init__(self, root: tk.Tk, width: int, height: int):
        self.root: tk.Tk = root
        self.width: int = width
        self.height: int = height
        self.display_panels: List[Panel] = []
        self.action_panels: List[Panel] = []

    def draw(self) -> None:
        for panel in self.display_panels:
            panel.draw()
        for panel in self.action_panels:
            panel.draw()

    def tick(self) -> None:
        for panel in self.display_panels:
            panel.tick()

    def add_display(self, panel: Panel):
        self.display_panels.append(panel)

    def add_action(self, panel: Panel):
        self.action_panels.append(panel)
