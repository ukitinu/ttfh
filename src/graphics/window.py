from __future__ import annotations

import logging
import sys
import tkinter as tk
import tkinter.messagebox
from typing import List

from src import ini, saves
from src.graphics import mainpanels
from src.graphics.interfaces import Panel
from src.timer import Clock

LOG = logging.getLogger(__name__)


class Window:
    _BG_COLOUR = '#000000'
    _MIN_WIDTH = 352
    _MIN_HEIGHT = 440

    _WIDTH = max(int(ini.gui("width")), _MIN_WIDTH)
    _HEIGHT = max(int(ini.gui("height")), _MIN_HEIGHT)
    _POS_X = int(ini.gui("pos-x"))
    _POS_Y = int(ini.gui("pos-y"))

    def __init__(self, clock: Clock):
        self.window = tk.Tk()
        self.clock = clock
        self.panel: Panel = mainpanels.create_main_panel(self.window, self.clock, self._WIDTH, self._HEIGHT)

    def _on_delete(self) -> None:
        """
        Creates the 'continue' file when the window is closed.
        """
        LOG.info('Closing')
        self.window.destroy()
        LOG.info('Saving')
        self._make_continue()
        sys.exit(0)

    def _make_continue(self) -> None:
        """
        Creates the 'continue' file.
        """
        save_time = f'--day {self.clock.day} --hour {self.clock.hour} --minute {self.clock.minute}'
        content = f'{ini.sys("entrypoint")} {save_time}'

        save_list = saves.serialize()
        if save_list:
            content += f' --saves="{save_list}"'

        with open('continue', 'w', encoding='utf-8') as batch_file:
            batch_file.write(f'{content}\n')

    def _tick(self):
        self.panel.tick()

    def _draw(self, save_errors: List[str]) -> None:
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

        def show_save_errors():
            if save_errors:
                tkinter.messagebox.showinfo(
                    title='Savestate errors',
                    message='Unable to restore the following saves:\n - ' + '\n - '.join(save_errors))

        self.window.after(self.clock.get_interval(), trigger_change)
        self.window.after(0, lambda: show_save_errors())
        self.window.mainloop()

    def create(self, save_string: str):
        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_delete)
        errors = saves.deserialize(save_string)
        self._draw(errors)
