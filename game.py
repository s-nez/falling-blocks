#!/usr/bin/python
from time import sleep
import curses
from time import time
from random import randint
from board import Board
from scoreboard import ScoreBoard

STEP_TIME = 0.5

stdscr = curses.initscr()
curses.start_color() # enable color support
curses.noecho()      # don't display pressed keys
curses.cbreak()      # don't wait for a newline to process input
stdscr.keypad(1)     # enable keypad mode (process special keys, like Home)
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
    game_board = Board(stdscr, 0, 0, 20, 20)
    score_board = ScoreBoard(game_board.status, 5, 25)

    quit = False
    last_game_step = time()
    while not quit and not game_board.game_over():
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
        elif c == ord('w'):
            game_board.rotate_block()

        game_board.update()
        score_board.update()

    if game_board.game_over():
        stdscr.addstr(10, 5, 'GAME OVER')
        c = stdscr.getch()
        while c != ord('q'):
            c = stdscr.getch()

finally:
    # Disable the curses-friendly terminal settings and close the window
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
