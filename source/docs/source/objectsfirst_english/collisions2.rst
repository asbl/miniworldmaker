Collisions and sensors II
****************************

A typical use case is to find out what kind of **token** has been touched.

There are several solutions to this problem:

Attribute token_type
===================

You can add an attribute `token_type` to all your objects:

.. code block :: python

    player2 = miniworldmaker.Token()
    wall = miniworldmaker.Token()
    player2.token_type = "actor"
    wall.token_type = "wall"

    @player1.register
    def on_sensing_token(self, other_token):
        if other_token.token_type == "actor":
            pass # do something
        elif other_token.token_type == "wall":
            pass # do something else

**Important!

With this access, you must give **every** object a `token_type` attribute.
  
Otherwise you also have to check if this is present at all, if you don't want your whole program to crash otherwise.

This can be done with:
.. code-block:: python

    if other_token.token_type and other_token.token_type == "actor":

If each token has the `token_type` attribute, then you can omit this query.
  

Listen
=======

You can add objects to a list to check if the touched object is in this list.

.. code block :: python

    walls = []
    player2 = miniworldmaker.Token()
    wall = miniworldmaker.Token()
    walls.append(wall)

    @player1.register
    def on_sensing_token(self, other_token):
        if other_token.token_type in walls:
            pass # do something


**Important!

With this access you have to make sure that deleted objects are also removed from the list, e.g. in the following way:
.. code-block:: python

    walls.remove(wall)
    wall.remove()


Classes
========

If you work with classes, the **miniworldmaker** takes some of the work off your hands, because it can now recognize for itself which **child class** of `token` an object is.

Here you can add the following method to your class:

.. code-block::

    def on_sensing_[class-name](self, other)

Example
--------

.. code block :: python

    # The other class has the name Torch
    def on_sensing_torch(self, torch):
        print("Sensing torch")
        # ...

View
========

* `Full example <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/07%20-%20sensors_2.py)>`_

