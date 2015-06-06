#!/usr/bin/python
"""Main game module"""
import curses
from time import time
from board import Board
from scoreboard import ScoreBoard
from keymap import KeyMap

STEP_TIME = 0.5
CONFIG_FNAME = 'falling_blocks.conf'

STDSCR = curses.initscr()
curses.start_color() # enable color support
curses.noecho()      # don't display pressed keys
curses.cbreak()      # don't wait for a newline to process input
STDSCR.keypad(1)     # enable keypad mode (process special keys, like Home)
curses.curs_set(0)   # make the cursor invisible
curses.halfdelay(5)  # wait only half a second between each getch

# Overload colors to make blocks
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_CYAN)
curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)

try:
    keys = KeyMap()
    keys.load_from_file(CONFIG_FNAME)

    GAME_BOARD = Board(STDSCR, 0, 0, 20, 20)
    SCORE_BOARD = ScoreBoard(GAME_BOARD.status, 5, 25)

    GAME_QUIT = False
    LAST_GAME_STEP = time()
    while not GAME_QUIT and not GAME_BOARD.game_over():
        CURRENT_TIME = time()
        if CURRENT_TIME - LAST_GAME_STEP > STEP_TIME:
            GAME_BOARD.advance_block()
            LAST_GAME_STEP = CURRENT_TIME

        USR_INPUT = STDSCR.getch()
        if USR_INPUT == keys.quit:
            GAME_QUIT = True
        elif USR_INPUT == keys.lshift:
            GAME_BOARD.lshift_block()
        elif USR_INPUT == keys.rshift:
            GAME_BOARD.rshift_block()
        elif USR_INPUT == keys.land:
            GAME_BOARD.land_block()
        elif USR_INPUT == keys.rotate:
            GAME_BOARD.rotate_block()

        GAME_BOARD.update()
        SCORE_BOARD.update()

    if GAME_BOARD.game_over():
        STDSCR.addstr(10, 5, 'GAME OVER')
        USR_INPUT = STDSCR.getch()
        while USR_INPUT != keys.quit:
            USR_INPUT = STDSCR.getch()

finally:
    # Disable the curses-friendly terminal settings and close the window
    curses.nocbreak()
    STDSCR.keypad(0)
    curses.echo()
    curses.endwin()
