# Events

Events are a central concept of the Miniworldmaker:

* Events can be used to query inputs (e.g. mouse clicks or
  keyboard inputs).
* With events, objects can communicate with each other (e.g. via
  messages)

## Register an event

For the board or a player to react to an event, it must be registered.
be registered.

This works in the same way as the `act()` method:

``` python
@player.register
def on_key_down_w(self):
    self.move()
```

This registers the `on_key_down_w` method, which checks whether the
key <kbd>w</kbd> has been pressed.

As soon as the key is pressed, the token `player` moves one step forward.
step forward.

As before: Each registered method needs as first parameter the keyword `self`.
the keyword `self` as first parameter and with this keyword you can
access attributes and methods of the object within the method.

### on_key_down and on_key_pressed

There are two functions `on_key_down(self, key)` and
`on_key_pressed(self, key)`:

* The function `on_key_down` is called exactly once when the
  key is pressed.
* The function `on_key_pressed`, on the other hand, is called again and again,
  as long as the key is pressed.

``` {note}
Both functions exist in the variant `on_key_down_b(self)`,
`on_key_pressed_c(self)` to query the pressing of a concrete key, and
as well as in the variant `on_key_down(self, key)`.
`on_key_pressed(self, key)` to process all keyboard queries.
```

### Example

``` python
import miniworldmaker

board = miniworldmaker.TiledBoard()
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

### Output

 <video controls loop width=100%>
  <source src="../_static/token_events.webm" type="video/webm">
  Your browser does not support the video tag.
</video>


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