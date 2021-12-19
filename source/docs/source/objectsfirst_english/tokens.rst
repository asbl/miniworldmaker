Game Figures
************

What are tokens?
================

A **Token** is a token on your game board.

All objects on your board are 'tokens' that can be moved around the board and that can communicate with each other.

Example: Create a token
-----------------------------

After you have created the game board, a `token`, *(i.e. a game piece)* is now placed on the board. This goes like this:

.. code-block:: python
    :lineno-start: 1
    :emphasize-lines: 8,9

    import miniworldmaker

    board = miniworldmaker.TiledBoard()
    board.columns = 20
    board.rows = 8
    board.tile_size = 42
    board.add_background("images/soccer_green.jpg")
    player = miniworldmaker.token()
    player.add_costume("images/player.png")

    board.run()


What happens here?
------------------

* In line 9, a player object is created.
  
* Line 10 assigns a costume to the player object.

The costume
==========

Every `board` has a `background`, every `token` has a `costume`. To make your tokens look different, you can *put* a costume on your token.

Example
--------

The instruction for this is:

.. code block:: python

    token_name.add_costume("path_to_image")


Note: `path_to_image` is a (relative path) to the image.
You should put your images in the subfolder `images`, then the image `image.png` in the subfolder `images` has the path `images/image.png`.

Result
--------

... image:: /_images/token.jpg
  :width: 100%
  :alt: First Token

FAQ
===

* My token is **misaligned**, what should I do?
   
  A token is aligned correctly if the image looks upwards. If the image is aligned in another direction by default, then you have two possibilities

* You can rotate the image with an image editor.
* You can change the orientation of the costume in Miniworldmaker. This can be done with `my_token.costume.orientation = 90`.
  Set the appropriate value for orientation so that the costume is oriented correctly.
* Sometimes it is also necessary to set that the token can rotate but the costume should always be oriented the same way. This can be done with `my_token.costume.is_rotatable = False`.

View
========

* --> More information. See :doc:`Key Concepts: boards <../key_concepts/tokens>`
* `More examples <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/1%20Costumes%20and%20Backgrounds>`_