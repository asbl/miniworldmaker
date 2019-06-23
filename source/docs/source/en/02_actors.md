Actors
=======

### Create a new Actor class

Next, an actor is placed on the board.

This is done as follows


```
class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")
```

  * The first line creates a new class as a child class of the class Actor.
  
  * In the third line, the __init__() method is created again,
   which is called when a new Player object is created.
   
  * Line 4 calls the parent class init() method,
   which initializes many things behind the scenes.
   
  * Row 5 then adds an image to the Player object.

### Add the actor to the playing field


  So far we have only created one template to create player objects.
  Now we want to create concrete objects and add them to the playing field.
    Add the __init__() method of the playing field class:

```
  player1 = Player(position = (3, 3)
```



Translated with www.DeepL.com/Translator