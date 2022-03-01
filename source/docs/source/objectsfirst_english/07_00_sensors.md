# Sensors

Tokens have **sensors**, with which they can sense their environment
and can e.g. detect other tokens at their position.

## Detect an object

A `token` can track another `token` at the same location by using the
function `on_sensing_token`.

``` python
@player.register
def on_sensing_token(self, other):
    print("Damage!!!!!")
    self.remove()
```

### What happens here?

* The function `on_sensing_token` will be called when the token
    detects another object at the same location.
* The parameter `other` is a reference to the found object, so that
    so that you can directly access attributes and methods of this object
    (e.g. with `other.move()`)

## Compare with found object

Often an action should only be executed if a *certain* object is found.
is found.

This goes for example like this:

``` {code-block} python
---
lineno-start: 1
---
@player1.register
def on_sensing_token(self, other):
    global player2
    if other == player2:
      print("I found you, player2!")
```

The comparison in line 6 checks whether the object **is** the same object
as `player2`.

``` {note}
**Excursus: Global Variables**: Normally variables are only known
only known within a method, e.g. to prevent side-effects when the same
side effects when accessing the same variable in different places.
variable in different places.
```

The approach with which variables from other program parts are accessed here is
is simple and intuitive - but later you will try to avoid it.
try to avoid this.

### Extensive example

The following code shows how you can prevent objects from moving through walls:

``` python
from miniworldmaker import *

board = TiledBoard()
board.columns = 8
board.rows = 2
board.speed = 30
player = token()
player.add_costume("images/player_1.png")

wall = token((4,0))
wall.add_costume("images/wall.png")

@player.register
def act(self):
    if player.position != (0,4):
        player.direction = "right"
        player.move()

@player.register
def on_sensing_token(self, other):
    if other==wall:
        self.move_back()
    

board.run()
```

 <video controls loop width=300px>
  <source src="../_static/wall.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## Other sensors

### Check boundaries of the playing field

You can also check if a character is at the borders of the playing field (or beyond).
playing field (or beyond it):

### Is the piece not on the playing field?###.

``` python
@player3.register
def on_sensing_not_on_board(self):
  print("Warning: I'm not on the board!!!")
```

Example:

The following program simulates a fish swimming around:

``` python
from miniworldmaker import *

board=TiledBoard()
board.columns = 4
board.rows = 1
board.add_background("images/water.png")
fish = token((0,0))
fish.add_costume("images/fish.png")
fish.costume.orientation = - 90
fish.direction = "right
@fish.register
def act(self):
    self.move()

@fish.register
def on_sensing_not_on_board(self):
    self.move_back()
    self.flip_x()
        
board.run()
```

 <video controls loop width=300px>
  <source src="../_static/flipthefish.webm" type="video/webm">
  Your browser does not support the video tag.
</video>


*Is the character at the boundaries of the playing field?*

``` python
@player4.register
def on_sensing_borders(self, borders):
  print("Borders are here!", str(borders))
```

If a character is at the position (0,0) the following is printed: `Borders are here!
is printed: `Borders are here! ['right', 'top']`

## FAQ

* My collisions are not detected, what can I do?

  First test if the method is called at all, e.g. with:

  ``python
  @player.register
  def on_sensing_token(self, token):
    print(token)
    ...
  ```

  If the `print` statement is not called, then the sensor does not work.
  the sensor does not work.

## Outlook

* More information. See [Key Concepts: Sensors](../key_concepts/sensors>)
