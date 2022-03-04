Costumes
########

Each :doc:`move <../key_concepts/movement>` has a costume that determines how the token is displayed.


Examples
=========


Example: Add a costume
----------------------

.. code-block:: python

  player = miniworldmaker.Token(position=(3, 4))
  player.add_costume("images/char_blue.png")

Example: Add a color as costume
-------------------------------

Instead of an image you can add a color as costume:

.. code-block:: python

  player = miniworldmaker.Token(position=(3, 4))
  player.add_costume((255,255,255,0))
  # (Color values are r, g, b, alpha)

Orientation
***********

Sometimes the pictures are misaligned for a costume. The default direction for a token is 0° (looking "up"). 

If your image is not correctly algined, you can change the orientation of the image.

Example: Change orientation of the image

.. code-block:: python

  player = miniworldmaker.Token(position=(3, 4))
  player.add_costume("images/char_blue.png")
  player.costume.orientation = -90
  # rotates costume 90 degrees counter-clockwise

Costume Attributes
******************

Costumes have attributes which change the display-behaviour:

* **costume.info_overlay**: Shows info overlay with border and direction
* **costume.is_rotatable**: Should the image be rotated when token is rotated?
* **costume.is_upscaled**: The image will be upscaled to token_size. The aspect ratio is maintained. 
* **costume.is_scaled**: The image will be scaled to token_size. The aspect ratio wil lbe changed.

Example: Change rotatable
--------------------------

.. code-block:: python

  player = miniworldmaker.Token(position=(3, 4))
  player.add_costume("images/char_blue.png")
  player.costume.is_rotatable = False

...more
========

* See: :doc:`Appearance <../api/appearance>` 
* See: :doc:`Costume <../api/appearance.costume>` 