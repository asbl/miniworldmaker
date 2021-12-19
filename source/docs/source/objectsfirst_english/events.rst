Events
**********

Events are a central concept of the Miniworldmaker:

* Events can be used to retrieve input (e.g. mouse clicks or keyboard input).
* With events objects can communicate with each other (e.g. via messages).

Register an event
=========================

For the board or a player to respond to an event, it must be registered.

This works in the same way as the `act()` method:

  .. code block:: python

    @player.register
    def on_key_down_w(self):
        self.move()
 
Here we register the method `on_key_down_w` which checks if the key w has been pressed.

As soon as the key is pressed, the token `player` moves one step forward.

As before: Every registered method needs the keyword `self` as first parameter and with this keyword you can access attributes and methods of the object within the method.

on_key_down and on_key_pressed
-------------------------------

There are two functions `on_key_down(self, key)` and `on_key_pressed(self, key)`:

* The `on_key_do``wn` function is called exactly once when the key is pressed.
* The `on_key_pressed` key, on the other hand, is called again and again as long as the key is pressed.

Both functions exist in the variant `on_key_down_b(self)` / `on_key_pressed_c(self)` to query the pressing of a concrete key as well as in the variant `on_key_down(self, key)`/`on_key_pressed(self, key)` to process all keyboard queries.

Send messages
------------------

With `send message(self, message)` you can send a global message to **all** objects and the board.
These messages can be processed with `on_message`.

Example:

  .. code block :: python

    @player.register
    def on_message(self, message):
        if message == "Example message":
            do_something()

View
--------

* `Full example <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/05%20-%20events.py>`_
* `More examples <https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/05%20-%20events.py>`_
* --> More information. See :doc:`Key Concepts: events <../key_concepts/events>`.