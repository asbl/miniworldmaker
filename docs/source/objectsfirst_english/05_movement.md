# Position, alignment and movement

In this chapter you will learn how to change the position and orientation of a token to move it.

## move() and position

There are two ways to move a token:

* You can use the `position` attribute to directly change the position of a token.
* The function `move` moves your token in the current direction.
You can set the current direction with `token.direction`, e.g. like this:

## position

You can change the position like this:

``` python
@player.register
def act(self):
    self.position = (100, 200) # places token at x = 100, y = 200
```

### Example

In this example the token is moved to a random position over and over again (every 50 frames):

``` python
import miniworldmaker as mwm
import random

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token((100, 100))
player.add_costume("images/target.png")
player.orientation = -90

@player.register
def act(self):
    if self.board.frame % 50 == 0: # every 50th frame:
        player.position = (random.randint(0, 400), random.randint(0, 400))

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/target1.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## x and y

Alternatively, you can directly change individual coordinates of the token with the attributes `x` and `y`:

``` python
@player.register
def act(self):
    self.x = 100 # places token at x = 100.
```

**Example

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((90,90))
player.add_costume("images/player.png")
player.costume.orientation = -90
@player.register
def on_key_down_w(self):
    player.y = player.y - 1

player2 = mwm.Token((180,180))
player2.add_costume("images/player.png")
player2.costume.orientation = -90
@player2.register
def on_key_pressed_s(self):
    player2.y = player2.y - 1
    
board.run()
```

 <video controls loop width=100%>
  <source src="../_static/keydown.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## The move() function

You can call the `move()` function in combination with the `direction` attribute or the `turn_left` or `turn_right` function:

`python
@player.register
def act(self):
    self.direction = "right" # can also be 90
    self.move()
    # Alternative with turn_left:
    self.turn_left(30) # turns 30° left
    self.move()
```

**Example

The token looks to the right and then moves one step forward:

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.direction = "right"
    self.move()

board.run()
```

 <video controls loop width=100%>
  <source src="../_static/moveright.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## move_left, move_right, ...

With the move() function, the `token` always moves to the current `direction`.

But you can also make the `token` move directly in a direction. This can be done with the functions `move_right()`, `move_left()`, `move_up()` and `m̀ove_down()`.

The program above would look like this:

` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.move_right()

board.run()
```

## move_in_direction

Alternatively you can move the token with `move_in_direction()` in any direction.

Example: The token moves diagonally upwards

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((100,100))
player.add_costume("images/player.png")
player.orientation = -90 # correct image orientation
@player.register
def act(self):
    self.move_in_direction(45)

board.run()

```

 <video controls loop width=100%>
  <source src="../_static/movedirection.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### Example: movement in mouse position

The following program uses the function `move_in_direction()` to control the token in the direction of the mouse pointer:

``` python
import miniworldmaker as mwm

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90

@player.register
def act(self):
    self.move_in_direction(self.board.get_mouse_position())

board.run()

```

 <video controls loop width=100%>
  <source src="../_static/followmouse.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## turn_left and turn_right

With `turn_left()` and `turn_right` you can turn the token in one direction.

* ``player.turn_left(degrees)`` - Turns the token **degrees** to the left.
* ``player.turn_right(degrees)`` - Turns the token **degrees** to the right.

Example:

``` python
import miniworldmaker as mwm

board = mwm.Board(400, 400)
board.add_background("images/grass.jpg")
player = mwm.Token((100, 100))
player.add_costume("images/player.png")
player.orientation = -90

@player.register
def act(self):
    self.move()
    
@player.register
def on_key_down_a(self):
    self.turn_left(30)

@player.register
def on_key_down_d(self):
    self.turn_right(30)


board.run()
```

 <video controls loop width=100%>
  <source src="../_static/turn.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## Direction

With `self.direction` you can query or change the current direction of the token
  
The value degrees can be specified here either as a number or as text as in the following graphic (0: up, 180, down, 90 right, -90 left):

![Move on board](/_images/movement.jpg)
  
Example:

In the following example the token moves in a circle:

``` python
import miniworldmaker as mwm

board = mwm.Board(400,400)
board.add_background("images/grass.jpg")
player = mwm.Token()
player.add_costume("images/player.png")
player.orientation = -90
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
