import curses
from random import randint
from copy import deepcopy

def gen_2d_array(height, width, default = 0):
    """
    Generate a list of lists with the specified size,
    optionally filled with a value other than 0
    """
    col = [default] * height
    arr = []
    for i in xrange(width):
        arr.append(deepcopy(col))
    return arr

def curses_draw_spot(win, y, x, color):
    """Draw a single-colored rectangle on the curses display"""
    win.addstr(y, x, ' ', curses.color_pair(color))

class Board(object):
    """
    The game board. The central object which controls spawning
    and movement of blocks as well as the heap of block remnants.
    """
    def __init__(self, stdscr, start_y, start_x, height, width):
        self.win = curses.newwin(height, width, start_y, start_x)
        self.win.box()
        stdscr.refresh()
        self.win.refresh()

        self.start_y = start_y
        self.start_x = start_x
        self.width = width
        self.height = height

        self.SHAPES = [
            [ [1, 1, 1], [0, 0, 1]   ],
            [ [0, 1], [1, 1], [0, 1] ],
            [ [1, 1], [1, 1]         ],
            [ [0, 0, 1], [1, 1, 1]   ],
            [ [1, 1, 1, 1]           ],
            [ [1, 1, 0], [0, 1, 1]   ]
        ]

        self.active_block = self.spawn_block()
        self.heap = Heap(1, 1, height - 2, width - 2)
        self.draw()

    def random_shape(self):
        """Pick a shape from the presets at random."""
        shape_index = randint(0, len(self.SHAPES) - 1)
        return self.SHAPES[shape_index]

    def spawn_block(self):
        """Create and return a new bock with random shape."""
        spawn_y = self.start_y + 1
        spawn_x = self.start_x + (self.width / 2)
        block = Block(self.random_shape(), 1, spawn_y, spawn_x)
        return block
    
    def out_of_bounds(self, y, x):
        """Check if the given location is outside the game board"""
        min_y, max_y = self.start_y , self.start_y + self.height - 1
        min_x, max_x = self.start_x , self.start_x + self.width - 1
        return y <= min_y or y >= max_y or x <= min_x or x >= max_x

    def block_movable(self, y, x):
        """
        Return if the active block can be safely moved into
        the specified location.
        """
        for ny, nx in self.active_block.gen_coords(y, x):
            if self.out_of_bounds(ny, nx) or self.heap.collision(ny, nx):
                return False
        return True

    def advance_block(self):
        """
        Move the active block block one square down. If the block cannot be
        moved, it is added to the heap and a new block is spawned. The function
        returns True if the block was moved, False otherwise.
        """
        y, x = self.active_block.position
        if self.block_movable(y + 1, x):
            self.active_block.set_position(y + 1, x)
            return True

        self.heap.add(self.active_block)
        self.active_block = self.spawn_block()
        return False

    def lshift_block(self):
        """Move the active block on square to the left, if possible."""
        y, x = self.active_block.position
        if self.block_movable(y, x - 1):
            self.active_block.set_position(y, x - 1)

    def rshift_block(self):
        """Move the active block on square to the right, if possible."""
        y, x = self.active_block.position
        if self.block_movable(y, x + 1):
            self.active_block.set_position(y, x + 1)

    def land_block(self):
        """Move the active block all the way down."""
        while self.advance_block():
            pass # wat

    def draw_active_block(self):
        """Draw the active block on the curses display."""
        color = self.active_block.color
        for y, x in self.active_block.coords():
            curses_draw_spot(self.win, y, x, color)

    def draw_heap(self):
        """Draw the block remnant heap on the curses display."""
        for y, x, color in self.heap.contents():
            curses_draw_spot(self.win, y, x, color)

    def draw(self):
        """Draw all the game elements and refresh the curses window."""
        self.draw_heap()
        self.draw_active_block()
        self.win.refresh()


class Heap(object):
    """Heap of block remnants."""
    def __init__(self, start_y, start_x, height, width):
        self.remnants = gen_2d_array(height, width)
        self.start_y = start_y
        self.start_x = start_x
        self.width = width
        self.height = height

    def adj_coords(self, y, x):
        """Adjust the coordinates to fit into the remnants 2d list."""
        return [y - 1, x - 1]

    def collision(self, y, x):
        """
        Returns true if the given coordinate is
        already occupied by a block remnant.
        """
        y, x = self.adj_coords(y, x)
        return self.remnants[x][y] != 0

    def add(self, block):
        """Add the given block to the heap of remnants."""
        for y, x in block.coords():
            self.remnants[x - self.start_x][y - self.start_y] = block.color

    def contents(self):
        """
        Generate lists of coordinates and colors of every block
        remnant in the heap.
        """
        y, x = self.start_y, self.start_x
        for x_offset, column in enumerate(self.remnants):
            for y_offset, color in enumerate(column):
                yield [y + y_offset, x + x_offset, color]
        return


class Block(object):
    """A moving game block."""
    def __init__(self, shape, color, y, x):
        self.shape = shape
        self.color = color
        self.set_position(y, x)

    def set_position(self, y, x):
        """Move the block to the designated position."""
        self.position = y, x

    def coords(self):
        """Return a list of coordinates of block elements."""
        return self.gen_coords(*self.position)

    def gen_coords(self, y, x):
        """
        Generate a list of coordinates of block elements,
        assuming the block is located at the given position.
        """
        for x_offset, column in enumerate(self.shape):
            for y_offset, spot in enumerate(column):
                if spot == 1:
                    yield [y + y_offset, x + x_offset]
        return
