Boards
======

There are different types of boards:

## Tiledboard

A Board for Games based on Tiles (Like Rogue-Like RPGs).

![tiled_board](../_images/tiled_board.jpg)

### Examples:

Creating a TiledBoard Object:

```
myboard = miniworldmaker.TiledBoard()
myboard.columns = 30
myboard.rows = 20
myboard.tile_size = 20
```

**Advanced:** Creating a TiledBoard-Subclass as Class:

  *  
    ```
    class MyBoard(miniworldmaker.TiledBoard):

        def on_setup(self):
            self.columns = 30
            self.rows = 20
            self.tile_size = 20
    ```

#### Attributes  

  * Every token on a TiledBoard has the size of exactly on one Tile. (If your tile_size is 40, every token has the size 40x40. )
  
  * The **position** of a token (*mytoken.position*) corresponds to the tile on which it is placed.
  
  * Two tokens **collide** when they are on the same tile.
  
## PixelBoard

A board for pixel accurate games.

![tiled_board](../_images/asteroids.jpg)

### Examples:

Creating a PixelBoard Object:

```
myboard = miniworldmaker.PixelBoard()
myboard.columns = 300
myboard.rows = 200
```

**Advanced:** Creating a PixelBoard-Subclass as Class:

  *  
    ```
    class MyBoard(miniworldmaker.PixelBoard):

        def on_setup(self):
            self.columns = 300
            self.rows = 200
    ```

#### Attributes

  * The position of a token on a PixelBoard is the pixel at center of token.
  
  * New tokens are created with top-left corner of token rect at position.
  
  * Two tokens collide when their sprites overlap.
