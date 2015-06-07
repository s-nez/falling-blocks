# Gameplay
## Basics
Place the falling blocks on the board, when a line is filled, it disappears.
Each time you clear a line, you earn points. The game goes on until
a newly appearing block has no way to move down (the board is filled in the
middle). As you progress, the game will gradually speed up.

## The score multiplier
Normally, clearing a single line earns you 100 points. Each time you clear
a line, the score multiplier is increased by 0.1, when you land a block
without clearing a line, the multiplier is decreased by 0.1 until it
gets back to 1.0. That means clearing several lines consecutively will yield
more points.

## Special blocks
Blocks with colors other than white have special properties.

### Red blocks
Red blocks explode when they land, they remove any adjacent block remnant
from the board upon landing and don't stay on the board. Use them to clean
up difficult structures or places with too many blocks.

### Green blocks
Green blocks grow upon landing. When you place a green block on the board,
it will fill any adjacent empty spaces to the sides and downwards.

### Blue blocks
Blue blocks pass through other blocks when falling, i.e. they don't collide
with other blocks, only with the board boundary.

### Yellow blocks
If a cleared line contains any yellow blocks, it counts as two lines.
Spread those blocks across multiple lines to maximize your score.
