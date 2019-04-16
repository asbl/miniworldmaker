Movements
==========



### Movement

The central function for moving is the move function.

Move has the following signature:

```
    def move(distance) -> BoardPosition:
```

This means
  
  * By default, an actor moves **self.speed** steps in the direction he's looking.
  
  * You can also set the distance it moves manually by using an integer value for the parameter distance.
  
  * The function returns the position on the playing field where the player is after the move.
 
 ### Methoden und Attribute

Moves an actor

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: move
   :noindex:
```