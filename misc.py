"""Miscelanous auxiliary functions"""
from copy import deepcopy
import curses

def gen_2d_array(height, width, default=0):
    """
    Generate a list of lists with the specified size,
    optionally filled with a value other than 0
    """
    col = [default] * height
    arr = []
    i = 0
    while i < width:
        arr.append(deepcopy(col))
        i += 1
    return arr

def reverse_range(start):
    """Generate a descending sequence of numbers from (start - 1) to 0"""
    return xrange(start - 1, -1, -1)

def curses_draw_spot(win, y_coord, x_coord, color):
    """Draw a single-colored rectangle on the curses display"""
    win.addstr(y_coord, x_coord, ' ', curses.color_pair(color))
