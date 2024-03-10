# Sensors

Tokens have **sensors**, with which they can sense their environment
and can e.g. detect other tokens at their position.

## Detect an object.

You can detect objects by calling the corresponding sensors directly.
This works for example like this:

``` python
import miniworldmaker as mwm

board = mwm.Board(200, 100)

r = mwm.Rectangle((10,10),50,100)
c = mwm.Circle((200,50),20)

@c.register
def act(self):
    self.move_left()

@r.register
def act(self):
    token = self.detect()
    if token:
        self.color = (255,0,0)

board.run()
```

The second `act()` method contains the sensor. With the method `self.detect` it is queried, which tokens
was found at the current position. If no token is found, the method returns `None`.

:::{note}
The statement `if token` is equivalent to
`if token != None`.
:::

If the rectangle detects another `token` with its sensors, then the color changes.

 <video controls loop width=300px>
  <source src="../_static/sensor.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

## Events

In the example above, tokens were *actively* searched for. Alternatively, you can register an event,
which is called automatically when the sensor of the token detects something:

The last program can be programmed using events like this:

``` python
from miniworldmaker import *

board = mwm.Board(200, 100)

r = mwm.Rectangle((10,10),50,100)
c = mwm.Circle((200,50),20)

@c.register
def act(self):
    self.move_left()
 
@r.register
def on_detecting(self, other):
    self.color = (255,0,0)

board.run()
```

What happens here?

* The registered function `on_detecting` will be called when the token
  detects another object at the same location.
* The parameter `other` is a reference to the found object. You can use this
  to find out which other token was found.

## What was found?

With the help of sensors and if-else branches you can find out what exactly was found.
This goes for example like this:

``` python
import miniworldmaker as mwm

board = Board(200, 100)

r = Rectangle((10,10),50,100)

c1 = mwm.ircle((200,50),20)
c2 = mwm.Circle((120,50),20)

@c1.register
def act(self):
    self.move_left()

@c2.register
def act(self):
    self.move_left()
    
@r.register
def on_detecting(self, other):
    if other == c1:
        self.color = (255,0,0)
    if other == c2:
        self.color = (0, 255,0)

board.run()
```

In the on_detect_token method it is checked whether `other` is the same object as `c1` or `c2`.

If this is true, the rectangle is colored accordingly.

 <video controls loop width=300px>
  <source src="../_static/sensor2.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

``` {note}
**Excursus: Global Variables**: Normally variables are only known
only known within a method, e.g. to avoid side effects when the same
side effects when accessing the same variable in different places.
variable in different places.


The approach with which variables from other program parts are accessed here is simple
is simple and intuitive - in the tutorial `classes_first` you will learn how to avoid this.
you will learn how to avoid this.
```

### Walls

The following code shows how you can prevent objects from moving through walls.
This can also be made possible with the help of sensors:

``` python
import miniworldmaker as mwm

board = mwm.TiledBoard()
board.columns = 8
board.rows = 2
board.speed = 30
player = mwm.Token()
player.add_costume("images/player_1.png")

wall = mwm.Token((4,0))
wall.add_costume("images/wall.png")

@player.register
def act(self):
    if player.position != (0,4):
        player.direction = "right"
        player.move()

@player.register
def on_detecting(self, other):
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
def on_not_detecting_board(self):
  print("Warning: I'm not on the board!!!")
```

Example:

The following program simulates a fish swimming around:

``` python
import miniworldmaker as mwm

board = TiledBoard()
board.columns = 4
board.rows = 1
board.add_background("images/water.png")
fish = mwm.Token((0,0))
fish.add_costume("images/fish.png")
fish.costume.orientation = - 90
fish.direction = "right
@fish.register
def act(self):
    self.move()

@fish.register
def on_not_detecting_board(self):
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
def on_detecting_borders(self, borders):
  print("Borders are here!", str(borders))
```

If a character is at the position (0,0) the following is printed: `Borders are here!
is printed: `Borders are here! ['right', 'top']`

## FAQ

* My collisions are not detected, what can I do?

  First test if the method is called at all, e.g. with:

  ``python
  @player.register
  def on_detecting(self, token):
    print(token)
    ...
  ```

  If the `print` statement is not called, then the sensor does not work.
  the sensor does not work.