# Values and variables

A `value` is something that is stored in the computer and can be manipulated by a computer program. In the following, values are referred to as ``objects`` and the words are used synonymously.

``` {note}
In other programming languages, a distinction is made between primitive data types, which can only be modified, and **objects**, which often also carry attributes and methods, such as the class ``board``, which has the attribute ``size`` and whose background can be used with the method `add_background`.

Python has the simple philosphy: everything is an object - Therefore, the term *value`` is generally used here.
```

Each value has a datatype which you can query, e.g. the following program returns:

``` python
from miniworldmaker import *
import random
board = Board((100,100))

print(type("Hello World"))
print(type(Line((10,10), (100,100))))
print(type(17))

board.run()
```

The following output on the command line:

```
<class 'str'>
<class 'tokens.shapes.Line'>
<class 'int'>
```

## Variables

In order for objects created in the computer to be retrievable, one must store where it can be found. On a technical level, this is done by storing the *location* of an object in the computer. In a programming language like Python, we use a name to retrieve objects.

``` python
line = Line((10,10), (100,100))
```

saves the line under the name line. If you now use the name line, you can access the variable and change the object.

For example, you have already changed the color of a line in the previous chapters:

``` python
line.fill_color = (255,0,0)
```

You can also calculate with numbers in the same way

``` python
a = 3
b = 4
print(a + b)
```

## Assignments

Assignments are written as:

``` python
c = a + b
```
Which means:

  - First the result on the right side is evaluated.

  - Then the result is stored in the variable on the left side.

According to the following program:

``` python
a = 3
b = 4
c = a + b
```

a has the value 3, b the value 4 and c the value 7.

In the same way you can change values of objects, e.g. the position of a circle. The following program lets you move a circle with the keys a and d to the left or right. The x-position is accessible via the name ``circle.x`` and can also be changed this way.

``` python
from miniworldmaker import *
import random
board = Board((100,100))

circle = Circle((50,50), 20)

@board.register
def on_key_pressed_a(self):
    circle.x = circle.x - 1

@board.register
def on_key_pressed_d(self):
    circle.x = circle.x + 1
    
board.run()
```

The line ``circle.x = circle.x + 1`` says the following: First calculate the value ``circle.x + 1`` (i.e. increase the x-coordinate of the circle by 1.) and save the result of this calculation back to ``circle.x``.

``` {note}
The = does not mean that the expression on the left and on the right is mathematically equal.
Instead, the result of the right side is evaluated first and the result of this calculation is stored in the variable on the left side.

One reads the expression ``a = b`` as b is **assigned** to a.

Some programming languages use a different character instead of the = character to avoid confusion for novice programmers.
```

## Usage

Wherever you have used a number or a text so far, you can also use variables directly, e.g.

``` python
a = 3
b = 4
line = Line((a, b), (5, 6))
```

This works whenever the **data type** of the variable matches the expected **data type**.


For example, the following code will result in an error:

``` python
a = 3
b = 4
line = Line(a, (5, 6))
```

Line expects a tuple but receives only an integer variable. Therefore the following error is output

```
miniworldmaker.exceptions.miniworldmaker_exception.TokenArgumentShouldBeTuple: First argument to create a token [position] should be a tuple.
```

The error tries to give you a hint what you did wrong, so often it helps to read the error messages.


## Range of validity - Scope

When programmers write larger programs -and often in a team-, the name of variables has a special meaning: How do you prevent other programmers from using your own variable names and even causing unforeseen side effects?

The answer is "validity ranges: A variable has different scopes depending on where it was defined:

  * A variable introduced inside a function has a local scope. It is visible **locally** within this function, but not within other functions.

  * A variable defined outside a function is **globally** visible and can be used in all functions of your program. **Caution**: If you want to access and modify global variables, you must use the keyword global.

  Here's how it works:

  ``` python
  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      print(a)
  board.run()
  ```
  
  The value 3 is printed.

  ````{warning}
  But this does not work, because in the assignment a is interpreted as a local variable (which was not defined)

  ``` python

  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      a = a + 1
      print(a)
  board.run()
  ```
  ````
  
  This works again because a is defined as a global variable and therefore the global variable is accessed.

  ``` python

  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      global a
      a = a + 1
      print(a)
  board.run()
  ```


