Timer
*****

With **timers** you can execute events **time controlled**. For example, if you want an action to occur not immediately, but with some milliseconds or seconds delay, you can use a timer.

.. note::
  Python also offers in the library `time` the function `time.sleep(...)`.

  But you should **not** use this function, because the global delay can lead to side effects.

Starting a timer
===================

You can start a timer like this:


.. code block:: python

  miniworldmaker.ActionTimer(24, player.move)

.. image:: /_images/actiontimer.png
  :width: 100%
  :alt: UML


The function receives 2 arguments:

* After `24` frames (1).
* ... the function `player.move` is executed (2).

The different timers
=======================

There are different types of timers:

ActionTimer
-----------

The ActionTimer calls a method with arguments after a given time and removes itself afterwards.

.. code block :: python

  miniworldmaker.ActionTimer(24, player.move, None)


LoopActionTimer
---------------

The LoopActionTimer does the same as the action timer, but the action is repeated over and over with equal intervals. If this loop is to end, the timer must be deleted:

* This is how you create a loop action timer. The first parameter specifies in which intervals the loop should be repeated.

  .. code block :: python

    loopactiontimer = miniworldmaker.LoopActionTimer(24, player.move)

* This is how you can remove a LoopActionTimer again.

  .. code block :: python
    
    loopactiontimer.unregister()



