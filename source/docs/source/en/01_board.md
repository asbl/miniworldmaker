The playing field
=============

Here we go!

## A first world

We create the first world. This works with the following code:

```
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_image(path="images/soccer_green.jpg")
board.speed = 30

board.run()
```

### What happens here?

  * In line 1 the miniworldmaker library is imported.
  * In line 3 a new **object** of type **TiledBoard** is created.
  * In line 2-6 the various attributes of the object are changed.
  * In line 10 the game is started. With and() a mainloop is started, which draws the board again and again.

### Result

That's how it looks:

![tiles](../_images/grid.jpg)

### Variant: Show the grid

If you like, you can also have the borders of the individual tiles displayed.
Change the method setup() in the class MyBoard:

```
    def setup()
        ...
        self.background.grid_overlay = True
```

### Outlook: PixelBoards and TiledBoards

There are several subclasses of the class board:

  * A PixelGrid is intended for pixel-precise representation of content.
  
  * A TiledBoard is intended for boards where the actors move on square tiles.
  
Most of the functions differ only slightly, since both boards are subclasses of the class **Boards**.

See [Boards](../key_concepts/boards.md)
