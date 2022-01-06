from __future__ import annotations

import sys
import tkinter as tk

from src import ini
from src.graphics import mainpanels
from src.graphics.panels import Panel
from src.timer import Clock


class Window:
    _BG_COLOUR = '#000000'
    _WIDTH = 320
    _HEIGHT = 400
    _POS_X = 100
    _POS_Y = 100

    def __init__(self, clock: Clock):
        self.window = tk.Tk()
        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_delete)
        self.clock = clock
        self.panel: Panel = mainpanels.create_main_panel(self.window, self.clock, self._WIDTH, self._HEIGHT)

    def _on_delete(self) -> None:
        """
        Creates the 'continue' file when the window is closed.
        """
        self.window.destroy()
        self._make_continue()
        sys.exit(0)

    def _make_continue(self) -> None:
        """
        Creates the 'continue' file.
        """
        save_time = f'--day {self.clock.day} --hour {self.clock.hour} --minute {self.clock.minute}'
        with open('continue', 'w', encoding='utf-8') as batch_file:
            batch_file.write(f'{ini.sys("entrypoint")} {save_time}\n')

    def _tick(self):
        self.panel.tick()

    def draw(self) -> None:
        """
        Draws, displays and updates the main window of the programme.
        """
        self.window.geometry(f'{self._WIDTH}x{self._HEIGHT}+{self._POS_X}+{self._POS_Y}')
        self.window.config(bg=self._BG_COLOUR)
        self.window.resizable(False, False)
        self.window.title('Till the Final Hour')

        self.panel.draw()

        def trigger_change():
            if self.clock.running:
                self.clock.update_time()
                self._tick()
            self.window.after(self.clock.get_interval(), trigger_change)

        self.window.after(self.clock.get_interval(), trigger_change)
        self.window.mainloop()
