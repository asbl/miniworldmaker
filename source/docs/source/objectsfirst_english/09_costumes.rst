Costumes
*******

Tokens and costumes
===================

Each token has one or more costumes. Costumes have multiple images that can be used to describe animations.

.. image:: ../_images/costumes.png
  :width: 100%
  :alt: First Token


The first costume
-----------------

With the function

.. code block :: python
  
  self.add_costume("images/image.jpg")


you can add a new costume.

If no costume has been added yet, this will automatically become your first costume.


Add more pictures to a costume
=========================================

You can add more images to a costume with the **costume.add_image** statement.
 
.. code block :: python

  self.costume.add_image("images/image_2.jpg")


Alternatively, you can directly add a list of images to a costume:

.. code block:: python

  self.costume.add_image(["images/image_1.jpg, images/image_2.jpg"])



Animations
===========

You can imagine 2D animations like a flip book. By changing the image of an actor/token in quick succession
of an actor/token is changed in quick succession, it makes it appear as if the actor is moving.

To do this, you must first add several images to a costume (see above).

Then you can animate the costume as follows:

.. code block:: python

  self.costume.is_animated = True
  self.costume.animation_speed = 10


Switch between costumes
--------------------------

Here's how to switch between two costumes:

.. code block:: python

  self.switch_costume()


The statement jumps to the next costume. You can also specify a number as a parameter to jump to a specific costume.


### Display of images

* There are several ways to customize the appearance of your image, e.g. whether it can be rotated, automatically scaled, etc.
* --> More information. See :doc:`Key Concepts: Costumes <../key_concepts/costumes>`.



