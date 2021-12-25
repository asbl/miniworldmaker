Physics
******

You can use the physics engine with the help of a 'physics board':

In a physics board, some movement and collision functions work slightly differently than on other boards:

Getting Started
==============

First create a physics board and a token in it:

.. code block:: python

  import miniworldmaker

  myboard = miniworldmaker.PhysicsBoard()
  myboard.size = 400, 300
  myboard.add_background((0,0,0,255))
  token = miniworldmaker.Token((200,200))
  token.size = (40, 40)
  token.position = (10, 10)
  token.add_costume((200,200,200,200))
  myboard.run()


The token will now drop down automatically. You can now change the properties of the room and the token.

How should the token be simulated?
====================================

There are 4 ways how to simulate tokens:

* "simulated": The simulation is completely taken over by the physics engine.
* Manual": The physics engine ignores the object, but collisions with the object are possible.
* "static": Like manual, but intended for objects that are moved very rarely (e.g. walls). If you create many objects of this type, the performance of objects of type "static" is higher than "manual".
* None: No simulation. The object is simply ignored and other objects can move "through the object".


*This description is still continued