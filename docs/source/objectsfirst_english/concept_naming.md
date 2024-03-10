# Concept: Naming and variables

## Naming

In the first chapter you have seen statements of the following kind:

``` python
board = mwm.Board()
```

The `=` character has a different function here than in mathematics.

* First the right side of the statement is executed. In this case a TiledBoard() object is created.

* In the second step, the created object is saved with the name `board`. You can always access the created object later using this `name`.

So names have a very special meaning in a programming language, they serve you as a storage for objects and data. By giving objects a name, you can access them again later. Such names are also called **variables**, because the object that can be accessed via the name can usually be changed in various ways.

In the simple case this can look like this:

``` python
a = 3
b = 2
c = a + b
```

By storing values under the names a and b, you can access them again later. In the last line, `a + b` is calculated first and the result is stored in `c`. The result is `5`.

Variables can store new values at any time - the old value will be lost:

` python
a = 3
a = 2
c = a + a
print(c)
```

The program prints `4` because the value 3 in the second line is overwritten and lost.

## The board object

The board is an object and has several attributes and methods
that you can access, e.g. `rows`, `columns` and `tile_size`.

### Attributes

Attributes are accessed with the syntax `object name.attribute name`.

Example:

``` python
board.rows = 4
```

This code stores the value 4 in `board.rows` - so the board object has 4 rows afterwards.

### Methods

Methods are commands that an object can execute, e.g. `board.add_background()` around
You access methods with the syntax `object name.method name()`. Sometimes there are variables in the parenthesis

Example:

``` python
board.add_background("images/my_background.png)
```

