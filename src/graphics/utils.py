import tkinter as tk


def draw_circle(canvas: tk.Canvas, x_coord: int, y_coord: int, ray: int, **kwargs) -> int:
    """
    Draws either a circle or a circle arc with the given centre and ray.
    If 'extent' is one of the kwargs, it draws an arc with the given size (in degrees), from the top. To go clockwise,
    use a negative value for extent.
    Otherwise, it draws a circle.

    :param canvas: canvas where the circle/arc is to be drawn
    :param x_coord: circle's centre x-coordinate
    :param y_coord: circle's centre y-coordinate
    :param ray: circle's ray
    :param kwargs: additional args shared by tkinter.Canvas::create_arc and tkinter.Canvas::create_oval
    :return: int returned by tkinter
    """
    if "extent" in kwargs:
        return canvas.create_arc(x_coord - ray, y_coord - ray, x_coord + ray, y_coord + ray,
                                 fill=None, start=90, style=tk.ARC, **kwargs)
    return canvas.create_oval(x_coord - ray, y_coord - ray, x_coord + ray, y_coord + ray, fill=None, **kwargs)


def calc_arc_extent(day: int, hour: int, minutes: int) -> int:
    """
    Returns the value, in degrees, to use to draw the arc representing the current minutes. It is negative to run
    clockwise.
    Hour and day are passed to handle the hedge cases.

    :param day: current day
    :param hour: current hour
    :param minutes: current minute
    :return: arc extent in degrees (int)
    """
    extent = -1 * minutes * 6
    if minutes == 0 and hour == 5 and day == 1:
        return 0
    if minutes == 0:
        return -359
    return extent
