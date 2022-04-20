# Concept: Functions

You have so far used methods that belong to a board or a token, e.g. ``on_setup``, ``act``.

## Defining functions

Often you want to automate complicated things, e.g. the creation of tokens.

You can do this by defining functions yourself - This works like this:

``` python
def create_token(x, y):
    t = token()
    t.position = (x,y)
    t.add_costume("images/player.png")
```

Your function consists of a *signature* and a *function body*.

*The signature is the first line of the function. It contains all the information
  you need to call the function. This is the **name** and **parameter**.
  The name of this function is `create_token`, the parameters are `x`and `y`.
  Parameters are needed to pass further information to the function, in this case
  the information **where** the token should be created.

* The function body is a code block. It contains all commands which are processed one after the other when the
  are processed one after the other.
  
  Here at the function call first a token is created and afterwards the properties of the token are defined.
  the properties of the token are defined.

## Call of functions

A function is called with the help of its name. Thereby you pass the arguments defined as parameters to the function.
This can look like this:

``` python
create_token(4,2)
```

Here a token is created at the position x=4 and y=2.

## Extensive example

The following example is a template to make your code shorter if you use functions.

Here 10 tokens with 10 commands are created. Without functions you would have needed 30 commands.

``` python
from miniworldmaker import *

board = TiledBoard()
board.rows = 8

def create_token(x, y):
    t = token()
    t.position = (x,y)
    t.add_costume("images/player.png")

def create_wall(x, y):
    t = token()
    t.position = (x,y)
    t.add_costume("images/wall.png")
    
create_token(4,2)
create_wall(4,4)
create_wall(5,4)
create_wall(6,4)
create_wall(6,3)
create_wall(6,2)
create_wall(6,1)
create_wall(5,1)
create_wall(4,1)
create_wall(3,1)

board.run()
```
