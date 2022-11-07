# Concept: loops

## The for loop

The for-loop repeats -simplified- a command n times:

### Example

The following loop is executed 5 times:

``` python
for i in range(5):
    print("I'm in a loop!")
```

The program gives the following output

```
I'm in a loop!
I'm in a loop!
I'm in a loop!
I'm in a loop!
I'm in a loop!
```

## The counter variable

You can use the variable i as a counter variable. It counts up (starting from 0):

### Example

``` python
for i in range(5):
    print(i)
```

The program gives the following output

```
0
1
2
3
4
```

## General form:

Generally written:

``` python
for i in range(max):
    <codeblock>
```

or

``` python
for i in range(min, max):
    <codeblock>
```

You can specify how many times the loop will be run or specify specific ranges:

### Examples: Drawing with loops

You can draw with loops:

``` python
from miniworldmaker import *

board = Board(200, 200)

for i in range(4):
    Circle((20 + 50 * i, 50), 20)
    
board.run()
```

<img src="../_images/processing/for_circles.png" alt="circles" width="260px">

### Checkerboard pattern

With the module operator you can check if a result is divisible by 2, namely
``x divisible by 2 exactly if x % 2 == 0`

This can be used to draw chessboard-like patterns by combining loops with an if query:

``` python
from miniworldmaker import *

board = Board(200, 50)

for i in range(4):
    rect = Rectangle((50 * i, 0), 50, 50)
    if i % 2 == 0:
        rect.color = (255,0,0, 255)
    else:
        rect.color = (255, 255, 255, 255)
    
board.run()
```

<img src="../_images/processing/checkers1.png" alt="checkers" width="260px">

### Graphs

Graphs can also be drawn in this way:

``` python
from miniworldmaker import *

board = Board(400, 400)


for x in range(400):
    gl = 0.5*x + 50
    y = 400 - gl
    Point((x, y))
    
board.run()
```

<img src="../_images/processing/graph.png" alt="graphs" width="260px">

### Nested loops

You can use nested loops to draw multidimensional patterns.

``` python
from miniworldmaker import *

board = Board(200, 200)

for i in range(4):
    for j in range(4):
        Circle((20 + 50 * i, 20 + 50 * j), 20)
    
board.run()
```

<img src="../_images/processing/nested.png" alt="nested loop" width="260px">