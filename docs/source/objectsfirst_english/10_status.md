# Status: game state/end of game/levels

## Status/Score

- Often you want to show the current score or something similar.

For this the **miniworldmaker** offers you special tokens, e.g.
Text or Number tokens.

### Create a text

You can create a text like this:

``` python
text = miniworldmaker.Text(position, string)
```

- position is a tuple with the upper left corner of the text
- string is a text that will be displayed.

On a pixelboard a text is scaled automatically.
On a tiledboard it will be displayed completely inside a tile
(and is probably too small for longer texts).

#### Example:

``` python
import miniworldmaker as mwm

board = mwm.Board(400,400)
hello_world = Text((100,100), "Hello world!")

board.run()
```

<img src="../_images/text1.png" width=260px alt="Texts"/>

### Modify a text

You can change the text at any time using the text attribute.

The following program always displays the last pressed button:

``` python
from miniworldmaker import *

board = mwm.Board(400,400)
key = Text((100,100), "")

@key.register
def on_key_down(self, key):
    print(key)
    self.text = key[0]

board.run()
```

<img src="../_images/text2.png" width=260px alt="Texts and Events"/>

## Numbers

You can display numbers on the screen with number tokens.

This works very similar to text. The following program for example
every time a key is pressed the displayed number is increased by 1:

``` python
from miniworldmaker import *

board = mwm.Board(400,400)
show_number = Number((100,100), 1)

@show_number.register
def on_key_down(self, key):
    n = self.get_number()
    self.set_number(n + 1)

board.run()
```



## End of game / level change

The following are typical end-of-game/level change actions:

- Clear the playing field
- Stop the game field.

The following commands are available for this:

- `board.stop()`: Stops the game board. No more actions will be executed
    and no events are queried.
- `board.start()`: This cancels a stop command.
- `board.is_running`: With this variable you can query the status of the board.
    of the board.
- `board.clear()`: This function removes all pieces from the board.
- `board.reset()`: The function clears the current board and creates a new board
    creates a new board with all the pieces as they were in
    [board.on_setup()]{.title-ref}.


