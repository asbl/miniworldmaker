Actions
********

You can create a board and design tokens on it until now. But they can't move yet.


The act() method
-----------------

The board and all tokens can be controlled by the ``act()`` method.
This method is called again and again (to be exact: Every ``board.speed`` time units) until the game is finished.

.. image:: ../_images/act.png
  :width: 100%
  :alt: First Token


When you create a token, you can use the decorator ``@register`` to add an ``act()`` method to the field or to your tokens:

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

Lines 12-14: The decorator ``@player.register`` binds the ``act`` method to the ``player`` object.

In a similar way you will later often register reactions to events on objects (e.g. reactions to keyboard or mouse inputs or collision checks).

.. image:: /_images/moving_token.gif
  :width: 100%
  :alt: First Token

Outlook
--------

* `Full example <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tutorial/03%20-%20actions.py>`_
* `More examples <https://codeberg.org/a_siebel/miniworldmaker_cookbook/src/branch/main/tests/2%20Movement>`_