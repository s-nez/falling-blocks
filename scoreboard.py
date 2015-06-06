"""
Scoreboard curses window and a shared object
for connection with the game board.
"""
import curses
from interfaces import Updatable

class GameStatus(object):
    """The game status, handles adding score and adjusting the multiplier."""
    def __init__(self):
        self.over = False
        self.score = 0
        self.score_mod_default = 100
        self.score_mod = self.score_mod_default

    def add_score(self, lines):
        """
        Increase the score according to the number of lines specified
        and adjust the score multiplier
        """
        if lines == 0:
            self.score_mod = self.score_mod_default
        else:
            self.score += lines * self.score_mod
            self.score_mod += 10 * lines

    def game_speed(self):
        """
        Calculates how fast the game should be, given the current score.
        """
        pass

class ScoreBoard(Updatable):
    """
    The score board, displays data from
    a GameStatus object as a curses window
    """
    def __init__(self, status, start_y, start_x):
        self.win = curses.newwin(5, 25, start_y, start_x)
        self.status = status
        self.win.addstr(0, 0, 'SCORE')
        self.win.addstr(4, 0, 'Multiplier: ')
        self.update_score()

    def update_score(self):
        """Display the score on the curses display"""
        self.win.addstr(1, 0, str(self.status.score))
        self.win.addstr(4, 13, str(float(self.status.score_mod) / 100) + 'x')
        self.win.refresh()

    def update(self):
        self.update_score()