Movement and alignment
************************
With the `act()` method you can move tokens in regular intervals. Now you learn how to move your tokens specifically in one direction.


The move() function
===================

The central function for moving is the `move()` function.

With the function `move()` you can move your object by one or more steps:


Example
--------

.. code block :: python

  @player.register
  def act(self):
      self.direction = 90
      self.move()


The object **player** now keeps looking to the right (90°, see :doc:`Key Concepts: Directions <../key_concepts/directions>` ) and then moves one step forward.


The keyword self
======================

In the code above you have seen that the method act expects the keyword `self` as parameter. All methods that belong to an object always get this keyword as the first paramer.

Then, within the method, attributes and methods of the object itself can be accessed with this keyword.

For example, `self.direction = 90` refers *to its own* orientation.

Change the direction
===================

You can change the direction with the following commands:

* `player.turn_left(degrees)` - Turns the token **degrees** to the left.
  
* `player.turn_right(degrees)` - Turns the token **degrees** to the right.
  
* `player.direction = degrees` - Gives the player object the absolute direction degrees.
  
  The value degrees can be specified here either as a number or as text as in the following graphic (0: up, 180, down, 90 right, -90 left):


  .. image:: /_images/movement.jpg
    :width: 100%
    :alt: Move on board


View
========

* --> More information. See :doc:`Key Concepts: Movement <../key_concepts/movement>`.
* --> More information. See :doc:`Key Concepts: Directions <../key_concepts/directions>`.
* `Full example <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/04%20-%20movement%20and%20direction.py)>`_.
* `More examples <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/2%20Movement>`_
