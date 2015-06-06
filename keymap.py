"""Keyboard bindings and config loading"""
class KeyMap(object):
    def __init__(self):
        self.set_default()

    def set_default(self):
        """Set all values to default"""
        self.quit = ord('q')
        self.lshift = ord('a')
        self.rshift = ord('d')
        self.land = ord('s')
        self.rotate = ord('w')

    def load_from_file(self, fname):
        """Load keybindings from a file"""
        self.set_default()
        # TODO: Actually load bindings from file
