Movement and alignment
************************

With the ``act()`` method you can move tokens in regular intervals. Now you learn how to move your tokens specifically in one direction.


The move() function
===================

The central function for moving is the ``move()`` function.

With the ``move()`` function you can move your object one or more steps:


Example
--------

.. code block :: python

  @player.register
  def act(self):
      self.direction = 90
      self.move()


The token **player** looks to the right (90°, see :doc:`Key Concepts: Directions <../key_concepts/directions>` ) and then moves one step forward.
This is repeated periodically when the act() method is called.

move_left, move_right, ...
==========================

With the move() function, the ``token`` always moves to the current ``direction``.

You can also make the ``token`` move directly in a direction. This can be done with the ``move_right()``, ``move_left()``, ``move_up()`` and ``m̀ove_down()`` functions.

Example
--------

This code moves the token in the act() method to the right:

.. code block:: python

  @player.register
  def act(self):
      self.move_right()

move_in_direction
=================

Alternatively you can move the token with ``move_in_direction()`` in any direction.

Example:
---------

This moves the token to the right (direction 90°). See :doc:`Key Concepts: Directions <../key_concepts/directions>` to find out more about directions.

.. code block :: python

  @player.register
  def act(self):
      self.move_in_direction(90)


The self keyword
======================

In the code above you saw that the method ``act`` expects the keyword ``self`` as parameter. All methods that belong to an object always get this keyword as the first paramer.

Then, within the method, this keyword can be used to access attributes and methods of the object itself.

Example:
---------

For example, ``self.direction = 90`` refers *to its own* orientation, ``self.move_in_direction()`` calls its own ``move_in_direction`` method.

Change the direction
===================

You can change the direction with the following commands:

* ``player.turn_left(degrees)`` - Turns the token **degrees** degrees to the left.
* ``player.turn_right(degrees)`` - Turns the token **degrees** to the right.
* ``player.direction = degrees`` - Gives the player object the absolute direction degrees.
  
  The value degrees can be specified here either as a number or as text as in the following graphic (0: up, 180, down, 90 right, -90 left):


  .. image:: /_images/movement.jpg
    :width: 100%
    :alt: Move on board


View
========

* More information. See :doc:`Key Concepts: Movement <../key_concepts/movement>`.
* More information. See :doc:`Key Concepts: Directions <../key_concepts/directions>`.
* `Full example <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/04%20-%20movement%20and%20direction.py>`_.
* `More examples <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tests/2%20Movement>`_
