import curses

class Block(object):
    def __init__(self, display, color, pos, shape):
        # The blocks shape: each sublist represents a column
        self.body = shape
        self.width = len(self.body)
        self.height = len(self.body[0])

        self.position = [1, 10] # TODO: adapt to board size
        self.display = display
        self.color = color

    def __body_paint__(self, color):
        y, x = self.position
        for x_offset, column in enumerate(self.body):
            for y_offset, spot in enumerate(column):
                if spot == 1:
                    self.display.addstr(y + y_offset, x + x_offset, ' ', color)
        self.display.refresh()

    def show(self):
        self.__body_paint__(curses.color_pair(self.color))

    def hide(self):
        self.__body_paint__(curses.color_pair(0))

    def move(self, new_y, new_x):
        self.hide()
        
        # Get the window limits
        min_y, min_x = self.display.getbegyx()
        height, width = self.display.getmaxyx()
        max_y, max_x = min_y + height, min_x + width

        if new_y > min_y and new_y + self.height < max_y:
            self.position[0] = new_y
        if new_x > min_x and new_x + self.width < max_x:
            self.position[1] = new_x

        self.show()

    def move_left(self):
        y, x = self.position
        self.move(y, x - 1)

    def move_right(self):
        y, x = self.position
        self.move(y, x + 1)

    def move_up(self):
        y, x = self.position
        self.move(y - 1, x)

    def move_down(self):
        y, x = self.position
        self.move(y + 1, x)

    def landed(self):
        max_y = self.display.getbegyx()[0] + self.display.getmaxyx()[0]
        return self.position[0] + self.height == max_y - 1
