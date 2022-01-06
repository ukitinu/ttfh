from __future__ import annotations

import sys
import tkinter as tk
from typing import Dict, Literal

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
    _TRANS_DURATION = 3

    def __init__(self, clock: Clock):
        self.window = tk.Tk()
        self.clock: Clock = clock
        self.panels: Dict[Literal['main', 'trans'], Panel] = {
            "main": mainpanels.create_main_panel(self.window, self.clock, self._WIDTH, self._HEIGHT),
            "trans": mainpanels.create_transition_panel(self.window, self.clock, self._WIDTH, self._HEIGHT)
        }
        self.active: Literal['main', 'trans'] = "main"
        self.trans_count: int = 0

        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_delete)

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
            batch_file.write(f'{ini.get_sys("entrypoint")} {save_time}\n')

    def _pick_panel(self) -> Panel:
        return self.panels[self.active]

    def _should_switch(self) -> bool:
        if self.active == "main":
            is_min = self.clock.minute == self.clock.START_MINUTE
            is_hour = self.clock.hour == self.clock.START_HOUR
            is_day = self.clock.day != self.clock.START_DAY
            return is_min and is_hour and is_day
        else:
            return self.trans_count >= self._TRANS_DURATION

    def _switch(self) -> None:
        self.active = "main" if self.active == "trans" else "trans"
        self.trans_count = 0
        self._pick_panel().draw()

    def _tick(self):
        self._pick_panel().tick()
        if self.active == "trans":
            self.trans_count += 1

    def draw(self) -> None:
        """
        Draws, displays and updates the main window of the programme.
        """
        self.window.geometry(f'{self._WIDTH}x{self._HEIGHT}+{self._POS_X}+{self._POS_Y}')
        self.window.config(bg=self._BG_COLOUR)
        self.window.resizable(False, False)
        self.window.title('Till the Final Hour')

        self._pick_panel().draw()

        def trigger_change():
            if self.clock.running:
                self.clock.update_time()
                self._tick()
            if self._should_switch():
                self._switch()
            self.window.after(self.clock.get_interval(), trigger_change)

        self.window.after(self.clock.get_interval(), trigger_change)
        self.window.mainloop()
