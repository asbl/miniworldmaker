The Board
==========

Here we go!

A first world
---------------

We create the first world. This works with the following code:

```
from miniworldmaker import *

class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        self.add_image(path="images/soccer_green.jpg")

board = MyBoard()
board.show()
```

First a new *class* MyBoard is created. This is a child class of TiledBoard
and allows you to build all sorts of games based on tiles.

  * Line 1: The **import** statement imports the MiniWorldMaker library.
  * Line 3: The own playing field is created as child class of the class Tiledboard.
  * Line 5-6: The __init__() method is called when a new object is created (i.e. here in line 7).
  
    At the beginning of the __init__() method, the method of the parent class is first called with super().__init__(),
  which determines the size of the playing field and the individual tiles.
  
  * Line 7: A background is added to your board. Make sure the file is on the specified path.

Depending on your background image, the result will look like this:

![tiles](_images/first.jpg)

### Display a grid

If you like, you can also have the borders of the individual tiles displayed.
Change the method __init__() in the class MyBoard:

```
    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        self.background.show_grid()
        self.add_image(path="images/soccer_green.jpg")
```

That's how it looks:

![tiles](_images/grid.jpg)