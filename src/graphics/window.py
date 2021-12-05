from __future__ import annotations

import sys
import tkinter as tk

from src import ini
from src import timedata
from src.graphics.button import Button
from src.graphics.switch import Switch
from src.timer import Timer


class Window:
    __BG_COLOUR = '#000000'
    __WIDTH = 320
    __HEIGHT = 400
    __POS_X = 100
    __POS_Y = 100

    __DAY_HEIGHT = 64
    __PERIOD_HEIGHT = 32
    __BTN_HEIGHT = 48
    __HOUR_HEIGHT = __HEIGHT - __DAY_HEIGHT - __PERIOD_HEIGHT - __BTN_HEIGHT

    def __init__(self, timer: Timer):
        self.window = tk.Tk()
        self.window.wm_protocol("WM_DELETE_WINDOW", self.__on_delete)

        self.timer = timer
        self.day = tk.StringVar(self.window, timedata.get_day(self.timer))
        self.period = tk.StringVar(self.window, timedata.get_period(self.timer))
        self.time = tk.StringVar(self.window, timedata.get_time(self.timer))
        self.slow_btn: Switch = None
        self.pause_btn: Switch = None
        self.reset_btn: Button = None
        self.forward_btn: Button = None
        self.backward_btn: Button = None

    def __on_delete(self) -> None:
        """
        Creates the 'continue' file when the window is closed.
        """
        self.window.destroy()
        self.__make_continue()
        sys.exit(0)

    def __make_continue(self) -> None:
        save_time = f'--day {self.timer.day} --hour {self.timer.hour} --minute {self.timer.minute}'
        with open('continue', 'w', encoding='utf-8') as batch_file:
            batch_file.write(f'{ini.get_sys("entrypoint")} {save_time}\n')

    def __tick(self):
        self.day.set(timedata.get_day(self.timer))
        self.period.set(timedata.get_period(self.timer))
        self.time.set(timedata.get_time(self.timer))

    @staticmethod
    def __draw_circle(canvas: tk.Canvas, x_coord: int, y_coord: int, ray: int, **kwargs):
        if "extent" in kwargs:
            return canvas.create_arc(x_coord - ray, y_coord - ray, x_coord + ray, y_coord + ray,
                                     fill=None, start=90, style=tk.ARC, **kwargs)
        return canvas.create_oval(x_coord - ray, y_coord - ray, x_coord + ray, y_coord + ray, fill=None, **kwargs)

    def __calc_arc_extent(self, minutes: int) -> int:
        extent = -1 * minutes * 6
        if minutes == 0 and self.timer.hour == 5 and self.timer.day == 1:
            return 0
        if minutes == 0:
            return -359
        return extent

    def __draw_day_canvas(self) -> None:
        day_canvas = tk.Canvas(self.window, width=self.__WIDTH, height=self.__DAY_HEIGHT, bg=self.__BG_COLOUR,
                               highlightthickness=0)
        text_id = day_canvas.create_text(self.__WIDTH / 2, self.__DAY_HEIGHT / 2,
                                         anchor=tk.CENTER,
                                         text=self.day.get().split(':')[0],
                                         fill=self.day.get().split(':')[1],
                                         font='Arial 24 bold')
        day_canvas.pack()

        def on_change(varname, index, mode):
            day_canvas.itemconfigure(text_id,
                                     text=self.day.get().split(':')[0],
                                     fill=self.day.get().split(':')[1])

        self.day.trace_add('write', on_change)

    def __draw_period_canvas(self) -> None:
        period_canvas = tk.Canvas(self.window, width=self.__WIDTH, height=self.__PERIOD_HEIGHT, bg=self.__BG_COLOUR,
                                  highlightthickness=0)
        text_id = period_canvas.create_text(self.__WIDTH / 2, self.__PERIOD_HEIGHT / 2,
                                            text=self.period.get().split(":")[0],
                                            fill=self.period.get().split(":")[1],
                                            font='Arial 18 bold')
        period_canvas.pack()

        def on_change(varname, index, mode):
            period_canvas.itemconfigure(text_id,
                                        text=self.window.getvar(varname).split(":")[0],
                                        fill=self.window.getvar(varname).split(":")[1])

        self.period.trace_add('write', on_change)

    def __draw_hour_canvas(self) -> None:
        hour_canvas = tk.Canvas(self.window, width=self.__WIDTH, height=self.__HOUR_HEIGHT, bg=self.__BG_COLOUR,
                                highlightthickness=0)
        text_id = hour_canvas.create_text(self.__WIDTH / 2, self.__HOUR_HEIGHT / 2,
                                          text=self.time.get().split(":")[0],
                                          fill='white',
                                          font='Arial 64')
        self.__draw_circle(hour_canvas, self.__WIDTH // 2, self.__HOUR_HEIGHT // 2, self.__WIDTH // 3,
                           outline='white',
                           width=8)
        arc_id = self.__draw_circle(hour_canvas, self.__WIDTH // 2, self.__HOUR_HEIGHT // 2, self.__WIDTH // 3,
                                    outline='red',
                                    width=6,
                                    extent=-1 * int(self.time.get().split(":")[1]) * 6)
        hour_canvas.pack()

        def on_change(varname, index, mode):
            hour = self.window.getvar(varname).split(":")[0]
            hour_canvas.itemconfigure(text_id, text=hour)

            minutes = int(self.window.getvar(varname).split(":")[1])
            extent = self.__calc_arc_extent(minutes)
            hour_canvas.itemconfigure(arc_id, extent=extent)

        self.time.trace_add('write', on_change)

    def __slow(self) -> None:
        self.timer.cycle_millis()
        self.slow_btn.set_on(self.timer.slow)

    def __pause(self) -> None:
        self.timer.un_pause()
        self.pause_btn.set_on(self.timer.running)

    def __reset(self) -> None:
        self.timer.reset()
        self.pause_btn.set_on(self.timer.running)
        self.slow_btn.set_on(self.timer.slow)
        self.__tick()

    def __fwd(self) -> None:
        self.timer.forward()
        self.pause_btn.set_on(self.timer.running)
        self.slow_btn.set_on(self.timer.slow)
        self.__tick()

    def __bwd(self) -> None:
        self.timer.backward()
        self.pause_btn.set_on(self.timer.running)
        self.slow_btn.set_on(self.timer.slow)
        self.__tick()

    def __draw_buttons(self) -> None:
        self.slow_btn = Switch(self.window, ini.get_img('slow-off'), ini.get_img('slow-on'), self.__slow)
        self.slow_btn.pack(side='left', padx=16, pady=10)
        self.pause_btn = Switch(self.window, ini.get_img('run-off'), ini.get_img('run-on'), self.__pause)
        self.pause_btn.pack(side='left', padx=16, pady=10)
        self.forward_btn = Button(self.window, ini.get_img('fwd'), self.__fwd).pack(side='right', padx=16, pady=10)
        self.backward_btn = Button(self.window, ini.get_img('bwd'), self.__bwd).pack(side='right', padx=0, pady=10)
        self.reset_btn = Button(self.window, ini.get_img('reset'), self.__reset).pack(side='right', padx=24, pady=10)

    def show(self) -> None:
        """
        Draws, displays and updates the main window of the programme.
        """
        self.window.geometry(f'{self.__WIDTH}x{self.__HEIGHT}+{self.__POS_X}+{self.__POS_Y}')
        self.window.config(bg=self.__BG_COLOUR)
        self.window.resizable(False, False)
        self.window.title('Countdown')

        self.__draw_day_canvas()
        self.__draw_period_canvas()
        self.__draw_hour_canvas()
        self.__draw_buttons()

        def trigger_change():
            if self.timer.running:
                self.timer.update_time()
                self.__tick()
            self.window.after(self.timer.get_interval(), trigger_change)

        self.window.after(self.timer.get_interval(), trigger_change)
        self.window.mainloop()
