"""Keyboard bindings and config loading"""
class KeyMap(object):
    """
    This class stores the game keybindings and handles loading the config file.
    """
    def __init__(self):
        self.quit = ord('q')
        self.lshift = ord('a')
        self.rshift = ord('d')
        self.land = ord('s')
        self.rotate = ord('w')

    def set_default(self):
        """Set all values to default"""
        self.quit = ord('q')
        self.lshift = ord('a')
        self.rshift = ord('d')
        self.land = ord('s')
        self.rotate = ord('w')

    def load_from_file(self, fname):
        """Load keybindings from a file"""
        try:
            opts = {}
            with open(fname, 'r') as fhandle:
                for line in fhandle:
                    line = line.rstrip()
                    action, key = line.split('=')
                    opts[action] = key
            self.quit = ord(opts['quit'])
            self.lshift = ord(opts['lshift'])
            self.rshift = ord(opts['rshift'])
            self.land = ord(opts['land'])
            self.rotate = ord(opts['rotate'])
        except (IOError, KeyError):
            self.set_default()
