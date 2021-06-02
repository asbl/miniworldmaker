Tokens
=======

### Create a new Token class

Next, an token is placed on the board.

This is done as follows

```
class Player(Token):

    def setup(self):
        self.add_image(path="images/char_blue.png")
```

  * Line 1 creates a new class as a child class of the class Token.
  
  * Line 3 defines the setup() method, 
  which is called when a new Player object is created.
  
  * A picture is then added to the Player object in line 4.

### Add the token to the playing field


  So far we have only created one template to create player objects.
  
  Now we want to create concrete objects and add them to the board.
    Add the setup() method of the playing field class:

```
class MyBoard(TiledBoard):

    def setup(self):
        ...
        player1 = Player(position = (3, 3))
```

Translated with www.DeepL.com/Translator (free version)