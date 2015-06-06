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
    win.addstr(y, x, ' ', curses.color_pair(color))

class Board(object):
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
        shape_index = randint(0, len(self.SHAPES) - 1)
        return self.SHAPES[shape_index]

    def spawn_block(self):
        spawn_y = self.start_y + 1
        spawn_x = self.start_x + (self.width / 2)
        block = Block(self.random_shape(), 1, spawn_y, spawn_x)
        return block
    
    def out_of_bounds(self, y, x):
        min_y, max_y = self.start_y , self.start_y + self.height - 1
        min_x, max_x = self.start_x , self.start_x + self.width - 1
        return y <= min_y or y >= max_y or x <= min_x or x >= max_x

    def block_movable(self, y, x):
        for ny, nx in self.active_block.gen_coords(y, x):
            if self.out_of_bounds(ny, nx) or self.heap.collision(ny, nx):
                return False
        return True

    def advance_block(self):
        y, x = self.active_block.position
        if self.block_movable(y + 1, x):
            self.active_block.set_position(y + 1, x)
            return True

        self.heap.add(self.active_block)
        self.active_block = self.spawn_block()
        return False

    def lshift_block(self):
        y, x = self.active_block.position
        if self.block_movable(y, x - 1):
            self.active_block.set_position(y, x - 1)

    def rshift_block(self):
        y, x = self.active_block.position
        if self.block_movable(y, x + 1):
            self.active_block.set_position(y, x + 1)

    def land_block(self):
        while self.advance_block():
            pass # wat

    def draw_active_block(self):
        color = self.active_block.color
        for y, x in self.active_block.coords():
            curses_draw_spot(self.win, y, x, color)

    def draw_heap(self):
        for y, x, color in self.heap.contents():
            curses_draw_spot(self.win, y, x, color)

    def draw(self):
        self.draw_heap()
        self.draw_active_block()
        self.win.refresh()


class Heap(object):
    def __init__(self, start_y, start_x, height, width):
        self.remnants = gen_2d_array(height, width)
        self.start_y = start_y
        self.start_x = start_x
        self.width = width
        self.height = height

    def adj_coords(self, y, x):
        return [y - 1, x - 1]

    def collision(self, y, x):
        y, x = self.adj_coords(y, x)
        return self.remnants[x][y] != 0

    def add(self, block):
        for y, x in block.coords():
            self.remnants[x - self.start_x][y - self.start_y] = block.color

    def contents(self):
        y, x = self.start_y, self.start_x
        for x_offset, column in enumerate(self.remnants):
            for y_offset, color in enumerate(column):
                yield [y + y_offset, x + x_offset, color]
        return


class Block(object):
    def __init__(self, shape, color, y, x):
        self.shape = shape
        self.color = color
        self.set_position(y, x)

    def set_position(self, y, x):
        self.position = y, x

    def coords(self):
        return self.gen_coords(*self.position)

    def gen_coords(self, y, x):
        for x_offset, column in enumerate(self.shape):
            for y_offset, spot in enumerate(column):
                if spot == 1:
                    yield [y + y_offset, x + x_offset]
        return
