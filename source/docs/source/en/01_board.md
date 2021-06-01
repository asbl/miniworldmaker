The playing field
=============

Here we go!

### A first world

We create the first world. This works with the following code:

```
from miniworldmaker import *


class MyBoard(TiledBoard):

    def setup(self):
        self.columns = 20
        self.rows = 8
        self.tile_size = 42
        self.add_image(path="images/soccer_green.jpg")

board = MyBoard()
board.show()
```

First a new *class* MyBoard is created. This is a child class of TiledBoard
and allows you to build all sorts of games based on tiles.

  * Line 1: The **import** statement imports the miniworldmaker library.
  * Line 4: The own playing field is created as child class of the class Tiledboard.
  * Line 6: The setup() method is called when a new object is created (i.e. here in line 7).
  * Lines 7-9: The size of the playing field is initialized.
  * Line 7: A background is added to your board. Make sure that the file is on the specified path.

These two lines:
```
board = MyBoard()
board.show()
```

The last two lines of your program are always similar: 
Here the MyBoard() command creates a concrete playing field, and then the
board.show() instructs the board to show itself.

Depending on your background image, the result will look like this:

![tiles](../_images/first.jpg)

### Show the grid

If you like, you can also have the borders of the individual tiles displayed.
Change the method setup() in the class MyBoard:

```
    def setup()
        ...
        self.background.grid_overlay = True
```

That's how it looks:

![tiles](../_images/grid.jpg)

### PixelBoards and TiledBoards

There are several subclasses of the class board:

  * A PixelGrid is intended for pixel-precise representation of content.
  
  * A TiledBoard is intended for boards where the actors move on square tiles.
  
Most of the functions differ only slightly, since both boards are subclasses of the class **Boards**.

```eval_rst
... inheritance-diagram:: miniworldmaker.boards.pixel_board.PixelBoard miniworldmaker.boards.tiled_board.TiledBoard
   :top-classes: miniworldmaker.tokens.boards.board
   :parts: 1
```



Translated with www.DeepL.com/Translator