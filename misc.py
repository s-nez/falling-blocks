"""Miscelanous auxiliary functions"""
import curses
from random import uniform, randint

def gen_2d_array(height, width, default_fill=0):
    """
    Generate a list of lists with the specified size,
    optionally filled with a value other than 0.
    >>> gen_2d_array(4, 4)
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    >>> gen_2d_array(2, 5)
    [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    >>> a = gen_2d_array(3, 3); a[0][0] = 1; a
    [[1, 0, 0], [0, 0, 0], [0, 0, 0]]

    >>> gen_2d_array(12, 1)
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    >>> gen_2d_array(12, 1, 'X')
    [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
    """
    arr = []
    for i in xrange(width):
        arr.append([])
        for _ in xrange(height):
            arr[i].append(default_fill)
    return arr

def reverse_range(start):
    """
    Generate a descending sequence of numbers from (start - 1) to 0.
    >>> reverse_range(10)
    xrange(9, -1, -1)

    >>> list(reverse_range(10))
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

    >>> list(reverse_range(0))
    []
    """
    return xrange(start - 1, -1, -1)

def curses_draw_spot(win, y_coord, x_coord, color):
    """Draw a single-colored rectangle on the curses display"""
    win.addstr(y_coord, x_coord, ' ', curses.color_pair(color))

def random_color():
    """Pick a color, which describes the block type, at random."""
    if uniform(0, 1) < 0.7: # 70% chance for a regular block
        return 1
    else:
        return randint(2, 7)
