# Configuration file
The game reads a file called 'falling\_blocks.conf' on startup.
This file should describe keybindings in a manner similar to Bash variables.

Example config:
```
lshift=a
rshift=d
land=s
rotate=w
quit=q
```

Left side assignment is a game action, right side is a key. A valid config
file should contain all of the above options, any additional ones
will be ignored. If one of the actions is missing or there is no
config file present, the default keybindings will be used.

## Default keybindings
* **A** - move block to the left
* **D** - move block to the right
* **S** - move the block all the way down
* **W** - rotate the block
* **Q** - quit the game
