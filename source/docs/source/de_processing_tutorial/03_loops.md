Lists and loops
====================

lists
------

### Create lists
A list contains several objects without you having to give each one a new name.

Example:

```
list = [0, 1, 2, 3, 4]
```

The list contains the numbers 0-4.

You can also create lists by first creating an empty list and then adding numbers one after the other:

```
list2 = []
list2.append(5)
list2.append(6)
list2.append(7)
```

This list contains the numbers 5, 6 and 7.

In the same way, a list can also contain objects of any kind.

```
cliste = []
cliste.append(Circle((40, 40), 60, 0, color=(255, 0, 0, 100))))
```

This adds a circle to a list.


### Accessing list items


The list elements can be accessed with a **index**:

```
list2 = []
list2.append(5)
list2.append(6)
list2.append(7)
print(list2[0], list2[1])
```

Spends 5 6. The 0th list element is 6, the 1st list element is 6.


Loops
---------

With the help of loops you can repeat things. For example, if you want to create 50 circles instead of 5,
the easiest way to do this is with a loop:

```
class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255)))
        for i in range(50):
            Circle((random.randint(0,260), random.randint(0,200)), 10, 0, color=(255, 0, 0, 100))
```

[![](../_images/replit.png)](https://repl.it/@a_siebel/circles)

The program creates 50 circles at random position.

With the help of lists you can also move all circles at the same time.
```
class MyBoard(ProcessingBoard):

    def on_setup(self):
        self.fill((255, 255, 255, 255)))
        self.lst = []
        for i in range(50):
            self.lst.append(Circle((random.randint(0, 800), random.randint(0, 600)), random.randint(10, 20), 0, color=(255, 0, 0, 100)))

    def act(self):
        for circle in self.lst:
            circle.y-=random.randint(0,2)
```
[![](../_images/replit.png)](https://repl.it/@a_siebel/circles2)

![](../_images/movingcircles.gif)
