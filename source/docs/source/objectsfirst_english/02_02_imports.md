# Specialist concept: Imports

With import you can import libraries and use the classes and functions stored there. There are different ways how you can import libraries:

## Different types of imports

You can import libraries in Python in different ways.
The following 3 statements are all allowed:

``python
import miniworldmaker
from miniworldmaker import *
import miniworldmaker as mwm
```

With the version used here ``import miniworldmaker`` you have to write ``miniworldmaker.object`` every time you import an object from the miniworldmaker library. Instead, you can also write ``from miniworldmaker import *`` - then you can omit miniworldmaker.

This is what the first program would look like if we had written ``import miniworldmaker``:

``{code-block} python
---
lineno-start: 1
---
import miniworldmaker
board = miniworldmaker.TiledBoard()
board.add_background("images/soccer_green.jpg")
board.columns = 20
board.rows = 8
board.tile_size = 40

board.run()
```

## Explicit vs. implicit.

The variant of writing `miniworldmaker.object` instead of just `object` each time
may seem uglier at first, because you have to write more text.

This is nevertheless the preferred variant in Python, since in this way it is possible to recognize
which objects were imported from which library.

It could be, for example, that you define a class 'TiledBoard' in your program.
the same name is used twice - for readers of your program it will be difficult to understand
difficult to understand what the name TiledBoard refers to.

In Python Zen the principle **explicit over implicit** is valid - This means that often more code is better
if this makes it more comprehensible.

## Aliases

The third variant is a compromise between the first and second variant.
If the name `miniworldmaker` is too long, you can define an alias, e.g. `mwm`.

The program would then look like this:

``{code-block} python
---
lineno-start: 1
---
import miniworldmaker as mwm
board = mwm.TiledBoard()
board.add_background("images/soccer_green.jpg")
board.columns = 20
board.rows = 8
board.tile_size = 40

board.run()
```

## Notes for teachers

Both variants are used in these tutorials. As a teacher you should decide
which variant you prefer for the start.

For beginners it can be helpful to do without this kind of imports.

