# Dynamics

You can create a board and design tokens on it until now.
But these can not move yet.

## The act() method

The board and all tokens can be controlled by the method `act()`.
method. This method is called again and again (exactly: All
`board.speed` time units) until the game is finished.

![First Token](../_images/act.png)

When you create a token, you can use the decorator `@register` to add an `act()` method to the token.
to add an `act()` method to the game field or to your tokens:

### Example

``{code-block} python
---
lineno-start: 1
---
from miniworldmaker import *

board = TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
player = token()
player.add_costume("images/player_1.png")
player.direction = 90
@player.register
def act(self):
    self.move()

board.run()
```

#### What happens here?

Lines 12-14: The decorator `@player.register` binds the `act` method
to the object `player`.

In a similar way you will later often register reactions to events on
objects (e.g. reactions to keyboard or mouse inputs or collision checks).
or collision checks).

 <video controls loop width=100%>
  <source src="../_static/moving_token.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## The keyword self

In the code above you saw that the ``act`` method expects the keyword ``self`` as a parameter.

All methods that belong to an object always get this keyword as the first paramer.

Then, within the method, attributes and methods of the object itself can be accessed with this keyword.

Example:

This code

``python
@player.register
def act(self):
    self.direction = "right"
```

is equivalent to this code:

``python
@player.register
def act(self):
    player.direction = "right"
```

``self`` here refers to the ``player`` object where the method was registered.

## The frame rate - how often is act() called?


You can set how often ``act()`` is called by configuring the ``board.fps`` and ``board.speed`` attributes.

* ``board.fps`` defines the ``frame rate``. Analogous to a flipbook, where you turn the pages at a fixed speed,
  the frame rate defines how many times per second the image is redrawn.
  ``board.fps`` has the default value 60, i.e. 60 frames per second are displayed.
  
* The attribute ``board.frame`` stores the current frame. The frames since program start are counted up.
  
* ``board.speed`` defines how often the program logic (e.g. act) is called per second.
  A value of 60 means that the act() method is called every 60th frame.


``python
  from miniworldmaker import *

  board = PixelBoard()
  board.size = (120,210)

  @board.register
  def on_setup(self):
      board.fps = 1
      board.speed = 3
      
  @board.register
  def act(self):
      print(board.frame)

  board.run()
```

The program above has the output:

```
  3
  6
  9
  12
  15
```


It is counted up very slowly, because exactly one frame per second is played and every 3. frame
(so every 3 seconds) the function ``act()`` is called.



## Outlook

- [Complete
    Example](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/03%20-%20actions.py)
- [More
    Examples](https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tests/2%20Movement)
