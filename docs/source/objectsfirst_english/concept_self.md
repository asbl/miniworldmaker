# The keyword self

In the code above you saw that the method ``act`` expects the keyword ``self`` as parameter.

All methods that belong to an object always get this keyword as their first paramer.

Then, within the method, attributes and methods of the object itself can be accessed with this keyword.

Example:

This code

``` python
@player.register
def act(self):
    self.direction = "right"
```

is equivalent to this code:

``` python
@player.register
def act(self):
    player.direction = "right"
```

`self` here refers to the `player` object where the method was registered.