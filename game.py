#!/usr/bin/python
from time import sleep
import curses
from block import Block
from time import time
from random import randint

SHAPES = [
        [ [1, 1, 1], [0, 0, 1] ],
        [ [0, 1], [1, 1], [0, 1] ],
        [ [1, 1], [1, 1] ],
        [ [0, 0, 1], [1, 1, 1] ],
        [ [1, 1, 1, 1] ],
        [ [1, 1, 0], [0, 1, 1]]
        ]

def spawn_block():
    shape_index = randint(0, len(SHAPES) - 1)
    block = Block(win, shape_index + 1, [1, 10], SHAPES[shape_index])
    block.show()
    return block

STEP_TIME = 0.5

stdscr = curses.initscr()
curses.start_color() # enable color support
curses.noecho()      # don't display pressed keys
curses.cbreak()      # don't wait for a newline to process input
stdscr.keypad(1)     # enable keypad mode (process special keys, like Home)
curses.curs_set(0)   # make the cursor invisible
curses.halfdelay(5)  # wait only half a second between each getch

# Overload colors to make blocks
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_CYAN)
curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)

BEGIN_X, BEGIN_Y = 0, 0
HEIGHT, WIDTH = 20, 20
win = curses.newwin(HEIGHT, WIDTH, BEGIN_Y, BEGIN_X)
win.box()
stdscr.refresh()
win.refresh()

quit = False
last_game_step = time()
block = spawn_block()
while not quit:
    current_time = time()
    if current_time - last_game_step > STEP_TIME:
        block.move_down()
        last_game_step = current_time

    c = stdscr.getch()
    if c == ord('q'):
        quit = True
    elif c == ord('a'):
        block.move_left()
    elif c == ord('d'):
        block.move_right()
    elif c == ord('s'):
        while not block.landed():
            block.move_down()

    if block.landed():
        block = spawn_block()

# Disable the curses-friendly terminal settings and close the window
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
