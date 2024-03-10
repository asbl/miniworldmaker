# Lists

Often we want to access many similar items at the same time e.g. months:

Suppose we want to store the average monthly temperatures in a city and we have measured the following data:

``` python

jan = 1.9
feb = 2.5
mar = 5.9
apr = 10.3
may = 14.6
jun = 18.1
jul = 20
aug = 19.6
sep = 15.7
oct = 10.9
nov = 6.2
dec = 2.8
```

If the data is to be processed further, then this becomes very impractical, since we have to "touch" each individual value each time. Therefore one uses lists instead.


For this purpose, lists are used in which similar elements are grouped together under a common **name** and can be accessed with the help of an **index**.

## What are lists?

Lists are a summary of data where each item is identified by an index. The individual values of a list are called *elements**.

### Create lists

You can create lists in Python in several ways. The simplest way is to create lists using square brackets:

``` python
l = [1, 2, 3]
l = ["mini", "worlds"]
```

Lists can themselves contain different data types, i.e. this is also a list:

``` python
l = ["hi", 1, 2, [3, 4]]
```

As you can see, it is even possible (and often necessary) to create a list within a list.

### Length of a list

You can calculate the length of a list with the len() function:

``` python
print(len([1, 2, 3])) # 3
print(len(["mini", "worlds"])) # 2
```

### Access elements

You can access elements of a list using the `index`. The syntax for this is as follows

``` python
variable_name[index]
```

e.g.

``` python
numbers = [2, 4, 8, 16, 32]
print(numbers[0]) # 2
print(numbers[2]) # 8
print(numbers[3]) # 16
```

### Change list elements

You can also modify list elements using the index:

``` python
numbers = [2, 4, 8, 16, 32]
numbers[0] = 1
print(numbers) # [1, 4, 8, 16, 32]
```

### append()

Lists in Python have a **dynamic** size and can be modified. So you can append an element to a list at any time with append():

``` python
numbers = [2, 4, 8, 16, 32]
numbers.append(64)
print(numbers) # [2, 4, 8, 16, 32, 64]
```

### in

With the keyword `in` you can check whether an element is contained in a list.

``` python
numbers = [2, 4, 8, 16, 32]
print(2 in numbers) # True
print(3 in numbers) # False
```

This is a significant difference to other programming languages, which know *arrays* as data structure instead of lists. Arrays are not changeable and have a fixed length.

## Example : Months

Let's take a closer look at the example of months. Instead of individual variables, you can create the months as a list:

``` python
months = []
months.append(1.9)
months.append(2.5)
months.append(5.9)
months.append(10.3)
months.append(14.6)
months.append(18.1)
months.append(20)
months.append(19.6)
months.append(15.7)
months.append(10.9)
months.append(6.2)
months.append(2.8)
```

Alternatively, you could create the list like this:
```python
months = [1.9, 2.5, 5.9, 10.3, 14.6, 18.1, 20, 19.6, 15.7, 10.9, 6.2, 2.8]
```

When we output the list, we get the following:

```
print(months)
> [1.9, 2.5, 5.9, 10.3, 14.6, 18.1, 20, 19.6, 15.7, 10.9, 6.2, 2.8]
```

We can access the individual list elements with an index:

``` python
print(months[1], months[4])
```

```
> 2.5 14.6
```

And we can iterate over the list with a loop. For example, we can calculate the average temperature:

``` python
for month in months:
    sum = sum + month
    
print(sum/12) # output 10.708
```

We can use this to visualize the data:

``` python
from miniworldmaker import *

board = Board(400, 240)

months = []
months.append(1.9)
months.append(2.5)
months.append(5.9)
months.append(10.3)
months.append(14.6)
months.append(18.1)
months.append(20)
months.append(19.6)
months.append(15.7)
months.append(10.9)
months.append(6.2)
months.append(2.8)

i = 0
for month in months:
    Rectangle((0,i), month * 10, 20)
    n = Number((200,i), month)
    n.font_size = 10
    i = i + 20
    
board.run()
```

![months](../_images/months.png)

## Save graphical objects

We can also store objects in arrays. This is often needed for collision detection, for example.

For example, we want to write a program where green circles should be collected and red dots should be avoided. We can implement this with lists as follows:

``` python
from miniworldmaker import *
import random

board = Board(400, 200)
points = Number((0,0), 0)

red_circles = []
green_circles = []

@board.register
def act(self):
    if self.frame % 100 == 0:
        c = Circle((400, random.randint(0,200), 40))
        c.color = (255, 0, 0)
        red_circles.append(c)
    elif self.frame % 50 == 0:
        c = Circle((400, random.randint(0,200), 40))
        c.color = (0, 255, 0)
        green_circles.append(c)
    for circle in red_circles:
        circle.move_left()
    for circle in green_circles:
        circle.move_left()

@board.register
def on_mouse_left(self, mouse_position):
    tokens = self.get_tokens_at_position(mouse_position)
    for token in tokens:
        if token in red_circles:
            token.remove()
            points.set_number(points.get_number() - 1)
        elif token in green_circles:
            token.remove()
            points.set_number(points.get_number() + 1)
            
board.run()
```

If you click the green circles, the score is increased by 1, otherwise it is decreased by 1.

The collision detection works with the help of lists: the circles are added to the red_circles and green_circles list respectively - This way you can use `circle in green_circles` to check if a circle is included in one of these two lists.

<video loop autoplay muted width="400">
<source src="../_static/collecting.webm" type="video/webm">
Your browser does not support the video tag.
</video>