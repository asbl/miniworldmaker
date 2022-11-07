# Movement and alignment

With the ``act(self)`` method you can move tokens in regular intervals. Now you learn how to move your tokens specifically in one direction.


## The move() function


The central function for moving is the `move()` function.

With the function `move()` you can move your object by one or more steps:


### Example

``` python
@player.register
def act(self):
    self.direction = "right"
    self.move()
```

The token `player` looks to the right and then moves one step forward.
This is repeated periodically when the act() method is called.

Complete example:

``` python
from miniworldmaker import *

board = TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
player = token()
player.add_costume("images/player_1.png")
@player.register
def act(self):
    self.direction = "right"
    self.move()

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/moving_token.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## move_left, move_right, ...

With the move() function, the `token` always moves to the current `direction`.

But you can also make the `token` move directly in a direction. This can be done with the functions `move_right()`, `move_left()`, `move_up()` and `m̀ove_down()`.

### Example

This code moves the token in the act() method to the right:

``` python
@player.register
def act(self):
    self.move_right()
```

## move_in_direction

Alternatively you can move the token in an arbitrary direction with `move_in_direction()`.

### Example:


This moves the token diagonally right upwards (direction 45°).

``` python
@player.register
def act(self):
    self.move_in_direction(45)
```

### Extensive example

Move in the direction of the mouse position:

``` python
import miniworldmaker

board = miniworldmaker.PixelBoard()
board.columns = 400
board.rows = 400
board.add_background("images/soccer_green.jpg")
player = miniworldmaker.Token()
player.add_costume("images/player_1.png")

@player.register
def act(self):
    self.move_in_direction(self.board.get_mouse_position())

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/followmouse.webm" type="video/webm">
  Your browser does not support the video tag.
</video>


## Change the direction


You can change the direction with the following commands:

  * ``player.turn_left(degrees)`` - Turns the token **degrees** to the left.

  * ``player.turn_right(degrees)`` - Turns the token **degrees** to the right.

  * ``player.direction = degrees`` - Gives the player object the absolute direction degrees.
  
  The value degrees can be specified here either as a number or as text as in the following graphic (0: up, 180, down, 90 right, -90 left):

![Move on the board](/_images/movement.jpg)
  
### Example:


`self.direction = 90` refers *to its own* orientation, for example, `self.move_in_direction()` calls its own `move_in_direction` method.

### Extensive example

In the following example, the token moves in a circle:

``` python
from miniworldmaker import *

board = PixelBoard()
board.columns = 400
board.rows = 400
board.add_background("images/soccer_green.jpg")
player = token()
player.add_costume("images/player_1.png")
player.position = (200, 200)

@player.register
def act(self):
    self.direction = self.board.frame
    self.move()
    

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/move_in_circle.webm" type="video/webm">
  Your browser does not support the video tag.
</video>