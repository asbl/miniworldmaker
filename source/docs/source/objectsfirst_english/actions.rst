The act() method
*****************

You can create a board until now and design tokens on it. But they can't move yet.


The act() method
-----------------

The board and all tokens can be controlled by the `act()` method.
This method is called again and again *(exactly: All `board.speed` time units)* until the game is finished.

.. image:: ../_images/act.png
  :width: 100%
  :alt: First Token


When you create a token you can add an `act()` method to the field or your tokens with the decorator `@register`:

.. code-block:: python
  :emphasize-lines: 12, 13, 14
  :lineno-start: 1

  import miniworldmaker

  board = miniworldmaker.TiledBoard()
  board.columns = 20
  board.rows = 8
  board.tile_size = 42
  board.add_background("images/soccer_green.jpg")
  board.speed = 30
  player = miniworldmaker.token()
  player.add_costume("images/player_1.png")
  player.direction = 90
  @player.register
  def act(self):
      self.move()

  board.run()


What happens here?
------------------

* Lines 12-14: The decorator `@player.register` binds the `act` method to the `player` object.

In a similar way you will later often register reactions to events on objects (e.g. reactions to keyboard or mouse inputs or collision checks).

Outlook
--------

* `Full example <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/03%20-%20actions.py>`_
* `More examples <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/2%20Movement>`_