# Branches

You always need branches when you want to check conditions and the program flow should depend on them.

### First example

For example, if you want to check whether a certain score has been reached in your game, this can be done with the following statement

``` python
if points > 100:
    print("You have won!")
```

### General syntax

In general, this is the syntax for branching:

``` python
if <condition>:
    <code block>
```
### Boolean expressions

A condition is an expression that can have the value `True` or `False`.
- Such expressions are called *boolean expressions*.

The simplest boolean expressions are `True` and `False`. You can usually get more expressions with **Compare**, e.g.:

``` python
10 < 100 # True
110 < 100 # False
x < 10 # True, if x < 10
"a" == "b" # False
3 == 4 # False
"ab" == "ab" # True
```

The expressions can be arbitrarily complicated and contain variables.

``` {warning}
Warning: In comparisons, always use a double equal sign instead of a single equal sign
```

### Comparisons

You can use the following comparisons:

* `<` : Less than
* `<=` : Less than or equal to
* `==`: Equal
* `>=` : Greater than or equal to
* `>` Greater than

### Code blocks

If you want to execute several statements depending on the condition, this can be done with the help of code blocks. Code blocks are always indented the same distance and all statements that are indented accordingly will be

Example:

``` python
if points > 100:
    print("You have won!")
    print("Congratulations")
print("The game is over")
```

Regardless of the score, the last line of code is executed in any case. However, the two indented lines are only executed if the score is greater than 100.

## Elif and Else

With elif and else you can insert alternatives. This goes for example like this:

``` python
if points > 100:
    print("You have won!")
    print("Congratulations")
elif points > 50:
    print("you lost by a narrow margin")
else:
    print("you have clearly lost)
```

The general syntax is:

``` python
if <condition>:
    <code block>
elif <condition>:
    <code block>
else <condition>:
    <code block>
```

Both elif and else can be omitted. Multiple elif blocks are also possible.

## Detailed example

A rectangle is to move from right to left. When it reaches the left side, it should reappear on the far right.

The first variant looks like this:

``` python
from miniworldmaker import *

board = Board(300, 200)

rect = Rectangle((280,120), 20, 80)

@rect.register
def act(self):
    rect.x -= 1


board.run()
```

The crucial part is still missing.

This can be formulated like this:

`If the x-coordinate reaches the value 0, set the rectangle to the right again`.

This can be translated directly into Python:

``` python
from miniworldmaker import *

board = Board(300, 200)

rect = Rectangle((280,120), 20, 80)

@rect.register
def act(self):
    rect.x -= 1
    if rect.x == 0:
        rect.x = 280

board.run()
```

## Another example - A simple Flappy Bird

We want to program a kind of (simple) Flappy-Bird.

Our main character should be a ball that moves upwards when the key is pressed.
We can realize this as follows:

``` python
from miniworldmaker import *

board = Board(300, 200)

rect = Rectangle((280,120), 20, 80)
ball = Circle((20,50),20)
velocity = 1
@rect.register
def act(self):
    rect.x -= 1
    if rect.x == 0:
        rect.x = 280

@ball.register
def act(self):
    global velocity
    self.y += velocity
    if board.frame % 10 == 0:
        velocity += 1
    
board.run()
```

The ball falls and falls faster and faster.

In the line:

``` python
    if board.frame % 10 == 0:
        velocity += 1
```

will increase the speed at which the ball falls.
In the first step the ball should be able to move upwards when a key is pressed.

``` python
from miniworldmaker import *

board = Board(300, 200)

rect = Rectangle((280,120), 20, 80)
ball = Circle((20,50),20)
velocity = 1
@rect.register
def act(self):
    rect.x -= 1
    if rect.x == 0:
        rect.x = 280

@ball.register
def act(self):
    global velocity
    self.y += velocity
    if board.frame % 10 == 0:
        velocity += 1

@ball.register
def on_key_down(self, key):
    global velocity
    velocity = -2
board.run()
```

### Colissions

Now we want to compare not only simple positions, but also the position of objects in relation to each other.

For this we can use various `sensor` methods.

This goes like this, for example:

``` python
from miniworldmaker import *

board = Board(300, 200)

rect = Rectangle((280,120), 20, 80)
ball = Circle((20,50),20)
velocity = 1
@rect.register
def act(self):
    rect.x -= 1
    if rect.x == 0:
        rect.x = 280

@ball.register
def act(self):
    global velocity
    self.y += velocity
    if board.frame % 10 == 0:
        velocity += 1
    token = self.detect_token()
    if token == rect:
       self.board.stop()

@ball.register
def on_key_down(self, key):
    global velocity
    velocity = -2
board.run()
```

The logic is in the following lines:

``` python
    token = self.detect_token()
    if token == rect:
       self.board.stop()
```

The first line checks with a sensor, which token was found at the own position (and returns the first found token).
Then the so found token is compared with the rect. If these are the same objects, then the game is stopped.

This is how the Flappy Bird game looks now:

 <video controls loop width=300px>
  <source src="../_static/flappy.webm" type="video/webm">
  Your browser does not support the video tag.
</video>