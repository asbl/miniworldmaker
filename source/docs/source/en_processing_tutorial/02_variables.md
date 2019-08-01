variables
== == == == =

Defining
Variables
--------------------

We
have
already
used
variables in the
previous
examples.

You
can
define
new
variables
by
writing:

```
self.variable
name = value
```

*The ** self ** always
refers
to
the
current
object.
For
example,
if you have created several circles, ** self ** means that the variable name
to * this * circle and to
no
other.
*A
variable is a ** Name **
for an object.An object can be a number, a word,
a
geometric
shape or much
more.By
giving
the
object
a
name,
you
can
access
it and change
it.

Consider
the
following
example:
```
from miniworldmaker import *


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.circle1 = Circle((40, 40), 60, 0, color=(255, 0, 0, 100))
        self.circle2 = Circle((80, 100), 60, 0, color=(0, 255, 0, 100))

    def on_mouse_left(self, mouse_pos):
        self.circle1.x = 150


my_board = MyBoard(400, 400)
my_board.show()
```

A
board
of
the
type
MyBoard
has
two
circles.By
giving
the
circles ** names **.
(namely self.circle1 and self.circle2)
you
can
also
access
the
circles
elsewhere.

Here
the
x - coordinate
of
the
first
circle is set
to
150.

![](.. / _images / movement.gif)

The
Random
Function
---------------------

The
Random
function
allows
you
to
assign
random
values
to
things.
First
you
have
to
randomly
import the

library
at
the
beginning
of
your
file:
```
import random

```

Then
a
single
command is sufficient
for the first one.

```
random.randint(0, 5)
```

This
creates
a
random
number
between
0 and 5

The
following
program
lets
a
circle
jump
to
a
random
position:
```
from miniworldmaker import *
import random


class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.circle1 = Circle((40, 40), 60, 0, color=(255, 0, 0, 255)))

        def on_mouse_left(self, mouse_pos):
            self.circle1.x = random.randint(0, 260)
            self.circle1.y = random.randint(0, 200)

    my_board = MyBoard(260, 200)
    my_board.show()

    ```