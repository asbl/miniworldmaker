# Acting and events

You can create a board and design tokens on it until now.
But they can't move yet.

For dynamic programs several functions are particularly relevant:

* The `on_setup()` method is called at the very beginning. This is where your board is set up and configured.
* The `act` method is called exactly once in each `frame`.
* There are several event methods, like `on_key_pressed`, `on_mouse_left`, `on_clicked_left`, ..., with which you can react to certain events.

## The act() method

The game field and all tokens can be controlled by the method `act()`.
method. This method is called again and again (exactly: All
`board.speed` time units) until the game is finished.

![First Token](../_images/act.png)

When you create a token, you can use the decorator `@register` to add an `act()` method to the token.
to add an `act()` method to the game field or to your tokens:

Example:

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((90,90))
player.add_costume("images/player.png")
@player.register
def act(self):
    player.y = player.y - 1

board.run()
```

<video controls loop width=100%>
  <source src="../_static/pixel_move1.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

:::{seealso}
[Here](concept_functions.md) you'll find a slightly more comprehensive explanation of how to write code with functions.
:::

### Orientation of a costume

You can see a problem here: The default orientation of the token is to *up*, but the image is oriented to *right*.

With the help of `token.costume.orientation` (or `token.orientation`) you can correct the orientation:

``` python
import miniworldmaker as mwm

board = mwm.Board()
board.add_background("images/grass.jpg")
player = mwm.Token((90,90))
player.add_costume("images/player.png")
player.costume.orientation = -90
@player.register
def act(self):
    player.y = player.y - 1

board.run()
```

Now the character runs looks in the direction it is moving.

 <video controls loop width=100%>
  <source src="../_static/pixel_move2.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

:::{seealso}
Inside methods, you can use `self` to call the attributes and methods of that particular object.
See [here](concept_self.md) for more on this.
:::

:::{seealso}
Using `board.speed` and `board.fps` you can set how often the board is redrawn
and how often `act()` is called, [see here](concept_framerate.md) more about this.
:::

## Events

Events are a central concept of the Miniworldmaker:

* Events can be used to query inputs (e.g. mouse clicks or
  keyboard inputs).
* With events, objects can communicate with each other (e.g. via
  messages)

### Register an event

In order for the board or a player to react to an event, it must be registered -like the
`act()` or `setup()` method- must be registered.

``` python
@player.register
def on_key_down_w(self):
    self.move()
```

This registers the `on_key_down_w` method, which checks whether the
key <kbd>w</kbd> has been pressed.

As soon as the key is pressed, the token `player` moves one step forward.
step forward.

Example:

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

board.run()
```

:::{note}
Every registered method needs as first parameter
the keyword `self`.
With this keyword you can
access attributes and methods of the object within the method, see also [self](concept_self.md)
:::

### Example

``` python
import miniworldmaker as mwm

board = mwm.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.token()
player.add_costume("images/player_1.png")
@player.register
def on_key_down_w(self):
    self.move()
@player.register
def on_key_down_a(self):
    self.turn_left()
@player.register
def on_key_down_d(self):
    self.turn_right()
@player.register
def on_key_down_s(self):
    self.move_back()
board.run()
```

Output:

 <video controls loop width=100%>
  <source src="../_static/token_events.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### on_key_down and on_key_pressed

There are two functions `on_key_down(self, key)` and
`on_key_pressed(self, key)`:

* `on_key_down` is called exactly once when the key is pressed.
* `on_key_pressed` on the other hand is called again and again as long as the key is pressed.

Example:

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

``` {note}
Both functions exist in the ``on_key_down_b(self)`` variant,
``on_key_pressed_c(self)`` to retrieve the pressing of a concrete key
as well as in the variant ``on_key_down(self, key)`` ``.
``on_key_pressed(self, key)`` to process all keyboard queries.
```

## Send messages

With `send message(self, message)` you can send a global message to
**all** objects and the board. These messages can be processed with
`on_message` to be processed.

Example:

``` python
@player.register
def on_message(self, message):
    if message == "Example message":
        do_something()
```