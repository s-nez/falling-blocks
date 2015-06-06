#!/usr/bin/python
from time import sleep
import curses
from time import time
from random import randint
from board import Board

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

try:
    game_board = Board(stdscr, 0, 0, 20, 20)

    quit = False
    last_game_step = time()
    while not quit:
        current_time = time()
        if current_time - last_game_step > STEP_TIME:
            game_board.advance_block()
            last_game_step = current_time

        c = stdscr.getch()
        if c == ord('q'):
            quit = True
        elif c == ord('a'):
            game_board.lshift_block()
        elif c == ord('d'):
            game_board.rshift_block()
        elif c == ord('s'):
            game_board.land_block()

        game_board.draw()

finally:
    # Disable the curses-friendly terminal settings and close the window
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
