"""The board module"""
import curses
from random import randint
from scoreboard import GameStatus
from misc import gen_2d_array, reverse_range, curses_draw_spot, random_color

class Board(object):
    """
    The game board. The central object which controls spawning
    and movement of blocks as well as the heap of block remnants.
    """
    def __init__(self, stdscr, start_pos, dimensions):
        # Very clean and totally maintainable code
        height, width = dimensions
        start_y, start_x = start_pos

        self.win = curses.newwin(height, width, start_y, start_x)
        self.win.box()
        stdscr.refresh()
        self.win.refresh()

        self.dim = [height, width]
        self.start_pos = [start_y, start_x]

        self.status = GameStatus()

        self.shapes = [
            [[1, 1, 1], [0, 0, 1]],
            [[0, 1], [1, 1], [0, 1]],
            [[1, 1], [1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1, 1, 1]],
            [[1, 1, 0], [0, 1, 1]]
        ]

        self.active_block = self.spawn_block()
        self.heap = Heap(1, 1, height - 2, width - 2)
        self.draw()

    def random_shape(self):
        """Pick a shape from the presets at random."""
        shape_index = randint(0, len(self.shapes) - 1)
        return self.shapes[shape_index]

    def spawn_block(self):
        """Create and return a new bock with random shape."""
        spawn_y = self.start_pos[0] + 1
        spawn_x = self.start_pos[1] + (self.dim[1] / 2)
        block = Block(self.random_shape(), random_color(), spawn_y, spawn_x)
        return block

    def out_of_bounds(self, coord_y, coord_x):
        """Check if the given location is outside the game board"""
        min_y = self.start_pos[0]
        max_y = self.start_pos[0] + self.dim[0] - 1
        min_x = self.start_pos[1]
        max_x = self.start_pos[1] + self.dim[1] - 1
        return coord_y <= min_y or coord_y >= max_y \
                or coord_x <= min_x or coord_x >= max_x

    def block_movable(self, coord_y, coord_x):
        """
        Return if the active block can be safely moved into
        the specified location.
        """
        for new_y, new_x in self.active_block.gen_coords(coord_y, coord_x):
            if self.out_of_bounds(new_y, new_x):
                return False

            # Blue 'ghost' block moves through the heap
            if self.active_block.color != 3 \
                    and self.heap.collision(new_y, new_x):
                return False
        return True

    def update_game_status(self):
        """Increase the score and check if the game should end."""
        self.status.add_score(self.heap.get_removed())

        coord_y, coord_x = self.active_block.position
        if not self.block_movable(coord_y + 1, coord_x):
            self.status.over = True

    def advance_block(self):
        """
        Move the active block block one square down. If the block cannot be
        moved, it is added to the heap and a new block is spawned. The function
        returns True if the block was moved, False otherwise.
        """
        coord_y, coord_x = self.active_block.position
        if self.block_movable(coord_y + 1, coord_x):
            self.active_block.set_position(coord_y + 1, coord_x)
            return True

        self.heap.add(self.active_block)
        self.active_block = self.spawn_block()
        self.update_game_status()
        return False

    def lshift_block(self):
        """Move the active block on square to the left, if possible."""
        coord_y, coord_x = self.active_block.position
        if self.block_movable(coord_y, coord_x - 1):
            self.active_block.set_position(coord_y, coord_x - 1)

    def rshift_block(self):
        """Move the active block on square to the right, if possible."""
        coord_y, coord_x = self.active_block.position
        if self.block_movable(coord_y, coord_x + 1):
            self.active_block.set_position(coord_y, coord_x + 1)

    def land_block(self):
        """Move the active block all the way down."""
        while self.advance_block():
            pass # wat

    def rotate_block(self):
        """Rotate the active block 90 degrees right"""
        coord_y, coord_x = self.active_block.position
        rotation = self.active_block.gen_rotation()
        for new_y, new_x in \
                self.active_block.gen_coords(coord_y, coord_x, shape=rotation):
            if self.out_of_bounds(new_y, new_x) or \
                    self.heap.collision(new_y, new_x):
                return
        self.active_block.rotate(rot=rotation)

    def draw_active_block(self):
        """Draw the active block on the curses display."""
        color = self.active_block.color
        for coord_y, coord_x in self.active_block.coords():
            curses_draw_spot(self.win, coord_y, coord_x, color)

    def draw_heap(self):
        """Draw the block remnant heap on the curses display."""
        for coord_y, coord_x, color in self.heap.contents():
            curses_draw_spot(self.win, coord_y, coord_x, color)

    def draw(self):
        """Draw all the game elements and refresh the curses window."""
        self.draw_heap()
        self.draw_active_block()
        self.win.refresh()

    def game_over(self):
        """Return the game status, True if game should end, False otherwise."""
        return self.status.over

    def game_speed(self):
        """Return the game step time in ms"""
        return self.status.game_speed()

class Heap(object):
    """Heap of block remnants."""
    def __init__(self, start_y, start_x, height, width):
        self.remnants = gen_2d_array(height, width)
        self.start_y = start_y
        self.start_x = start_x
        self.width = width
        self.height = height
        self.removed = 0

    def adj_coords(self, coord_y, coord_x):
        """Adjust the coordinates to fit into the remnants 2d list."""
        return [coord_y - self.start_y, coord_x - self.start_x]

    def collision(self, coord_y, coord_x):
        """
        Returns true if the given coordinate is
        already occupied by a block remnant.
        """
        coord_y, coord_x = self.adj_coords(coord_y, coord_x)
        return self.remnants[coord_x][coord_y] != 0

    def line_full(self, line_index):
        """Check if the line with given index is full."""
        for column in self.remnants:
            if column[line_index] == 0:
                return False
        return True

    def remove_full_lines(self):
        """Remove each full line from the heap."""
        lines_to_remove = set()
        for index in xrange(len(self.remnants[0])):
            if self.line_full(index):
                lines_to_remove.add(index)

        yellow_blocks = 0
        col_index = len(self.remnants[0]) - 1
        for index in reverse_range(len(self.remnants[0])):
            if not index in lines_to_remove:
                for column in self.remnants:
                    column[col_index] = column[index]
                col_index -= 1
            else: # Lines with yellow blocks count double
                for column in self.remnants:
                    if column[index] == 5:
                        yellow_blocks += 1
                        break
        self.removed += len(lines_to_remove) + yellow_blocks

    def in_heap(self, coord_y, coord_x):
        """
        Check if the specified coordinate is not outside the heap boundary.
        """
        if coord_y < 0 or coord_y >= len(self.remnants):
            return False
        if coord_x < 0 or coord_x >= len(self.remnants[0]):
            return False
        return True

    def empty_spot(self, coord_y, coord_x):
        """
        Check if the specified spot is empty, i.e. there is no block
        remnant occupying it.
        """
        return self.in_heap(coord_y, coord_x) \
                and self.remnants[coord_x][coord_y] == 0

    def add(self, block):
        """Add the given block to the heap of remnants."""
        for coord_y, coord_x in block.coords():
            coord_y, coord_x = self.adj_coords(coord_y, coord_x)
            self.remnants[coord_x][coord_y] = block.color
        if block.color == 2:
            # Green 'growing' block
            for coord_y, coord_x in block.coords():
                coord_y, coord_x = self.adj_coords(coord_y, coord_x)
                for grow_x in [coord_x - 1, coord_x + 1]:
                    for grow_y in [coord_y, coord_y + 1]:
                        if self.empty_spot(grow_y, grow_x):
                            self.remnants[grow_x][grow_y] = block.color
        elif block.color == 7:
            # Red 'exploding' block
            for coord_y, coord_x in block.coords():
                coord_y, coord_x = self.adj_coords(coord_y, coord_x)
                for destroy_x in [coord_x - 1, coord_x, coord_x + 1]:
                    for destroy_y in [coord_y - 1, coord_y, coord_y + 1]:
                        if self.in_heap(destroy_y, destroy_x):
                            self.remnants[destroy_x][destroy_y] = 0

        return self.remove_full_lines()

    def contents(self):
        """
        Generate lists of coordinates and colors of every block
        remnant in the heap.
        """
        coord_y, coord_x = self.start_y, self.start_x
        for x_offset, column in enumerate(self.remnants):
            for y_offset, color in enumerate(column):
                yield [coord_y + y_offset, coord_x + x_offset, color]
        return

    def get_removed(self):
        """
        Get the number of removed lines and reset the inner counter.
        """
        result = self.removed
        self.removed = 0
        return result

class Block(object):
    """A moving game block."""
    def __init__(self, shape, color, coord_y, coord_x):
        self.shape = shape
        self.color = color
        self.position = coord_y, coord_x

    def set_position(self, coord_y, coord_x):
        """Move the block to the designated position."""
        self.position = coord_y, coord_x

    def coords(self):
        """Return a list of coordinates of block elements."""
        return self.gen_coords(*self.position)

    def gen_coords(self, coord_y, coord_x, shape=None):
        """
        Generate a list of coordinates of block elements,
        assuming the block is located at the given position.
        """
        if shape == None:
            shape = self.shape

        for x_offset, column in enumerate(shape):
            for y_offset, spot in enumerate(column):
                if spot == 1:
                    yield [coord_y + y_offset, coord_x + x_offset]
        return

    def rotate(self, rot=None):
        """Rotate the block 90 degrees right"""
        if rot == None:
            rot = self.gen_rotation()
        self.shape = self.gen_rotation()

    def gen_rotation(self):
        """Generate a rotated shape for the block."""
        new_shape = []
        for index in reverse_range(len(self.shape[0])):
            new_column = []
            for column in self.shape:
                new_column.append(column[index])
            new_shape.append(new_column)
        return new_shape
