# Sensors II

A typical use case is to find out *which kind* of
**token** has been touched.

There are several solutions for this problem:

## 1. adding an attribute

You can add an attribute to all your objects, e.g. with the name
`token_type`:

``` python
player2 = miniworldmaker.Token()
wall = miniworldmaker.Token()
player2.token_type = "actor"
wall.token_type = "wall"

@player1.register
def on_detect_token(self, other_token):
    if other_token.token_type == "actor":
        pass # do something
    elif other_token.token_type == "wall":
        pass # do something else
```

````{warning}
With this access, you must give **every** object a `token_type` attribute.
to each object.

Otherwise you also have to check if it exists at all,
if you don't want your whole program to crash otherwise.
crashes.

This can be done with:

``` python
if other_token.token_type and other_token.token_type == "actor":
```

If each token has the attribute `token_type`, then you can omit this
omit this query.
````

## 2. using lists

You can add objects to a list to check if the touched object is in the list.
touched object is in this list.

``` python
walls = []
player2 = miniworldmaker.Token()
wall = miniworldmaker.Token()
walls.append(wall)

@player1.register
def on_detect_token(self, other_token):
    if other_token.token_type in walls:
        pass # do something
```

````{warning}
With this access you have to make sure that deleted objects are removed from the list
are removed from the list, e.g. in the following way:

``` python
walls.remove(wall)
wall.remove()
```
````

## Outlook: Classes

If you work with classes, the **miniworldmaker** will do some work for you
work for you, because it can now recognize which **child class** of `token
of `token` an object is.

Here you can add the following method to your class:

``` python
def on_detecting_[class_name](self, other)
```

### Example

``` python
# The other class has the name Torch
def on_detecting_torch(self, torch):
    print("Sensing torch")
    # ...
```
