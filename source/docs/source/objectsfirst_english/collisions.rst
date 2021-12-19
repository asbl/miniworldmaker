Collisions and sensors
************************

In addition to reacting to events, tokens can also use **sensors** to check whether other tokens are in the same place, for example.

Detect an object
====================

A `token` can track down another `token` at the same location as follows:

.. code block:: python

  @player.register
  def on_sensing_token(self, other):
      print("Damage!!!!!")
      self.remove()

What happens here?
------------------

* The function `on_sensing_token` is called when the token detects another object at the same location.
* The parameter `other` is a reference to the found object, so you can directly access attributes and methods of this object (e.g. with `other.move()`)

Compare with found object
==================================

Often an action should only be executed if a *certain* object is found.

This goes like this, for example:

.. code-block:: python
  :emphasize-lines: 1,5,6
  :lineno-start: 1

  player 2 = miniworldmaker.token()
  #...
  @player1.register
  def on_sensing_token(self, other):
      global player2
      if other == player2:
        print("I found you, player2!")


The comparison in line 6 checks if the object is **the same** object as `player2`.

... note::
   **Excursus Global Variables**: Normally variables are only known within a method, so that e.g. it is prevented
   to avoid side effects when accessing the same variable in different places.
   
   The approach with which variables from other program parts are accessed here is simple and intuitive.
   But later one will try to avoid this.

Check boundaries of the playing field
---------------------------------

You can also check if a piece is at the borders of the playing field (or beyond):

*Is the piece not on the board?*.

.. code block:: python

   @player3.register
   def on_sensing_not_on_board(self):
     print("Warning: I'm not on the board!!!")


*Is the character on the boundaries of the board?*.

.. code block :: python

  @player4.register
  def on_sensing_borders(self, borders):
    print("Borders are here!", str(borders))


If a character is at position (0,0) the following is printed: `Borders are here! ['right', 'top']`

FAQ
====
  * My collisions are not recognized, what can I do?
    * First test if the method is called at all, e.g. with:

    .. code-block:: python
    
      @player.register
      def on_sensing_token(self, token):
        print(token)
        ...
    

    If the `print` statement is not called, then the sensor does not work.


Outlook
=========


* --> More information. See :doc:`Key Concepts: Sensors <../key_concepts/sensors>`.
* The objects can be tracked in different ways.
  This can be set via the `collision_type` property of the object being tracked,
  e.g. 'mask' for a pixel-exact comparison or 'rect' if only the enclosing rectangles are compared.
  



