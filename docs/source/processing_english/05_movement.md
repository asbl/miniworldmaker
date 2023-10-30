# Movement

In this chapter we set elements in motion. Variables also help us to do this.

## Simple movements

You can realize a simple movement by changing the attributes x and y of an object.

``` python
from miniworldmaker import *
import random
board = Board((100,100))
c = Circle((0,50), 20)
@board.register
def act(self):
    c.x = c.x + 1
    
board.run()
```
Output:

<img src="../_images/processing/moving.gif" alt="moving" width="260px">

## The modulo operator

For repetitive movements, the modulo operator is particularly useful.

Python knows 3 types of divisions:

13 / 3 yields the result 4.33333333
13 // 3 returns the **integer** result 4
13 % 3 returns the remainder of the division 13 / 3, i.e. 1.

That the remainder can never be greater than the dividend can help us with animations:

``` python
from miniworldmaker import *
import random
board = Board((100,100))
c = Circle((0,50), 20)
x = 0
@board.register
def act(self):
    global x
    c.x = x % 100
    x = x + 1
board.run()
```

The variable x counts up and up, since the remainder of the division of x and 100 can never be greater than 100, the point moves back again.

<img src="../_images/processing/modulo.gif" alt="moving" width="260px">