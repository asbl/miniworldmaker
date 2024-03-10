# Timer

With **timers** you can execute events **time controlled**. If you
e.g. want an action to occur not immediately, but with a delay of some
milliseconds or seconds delay, you can use a timer.
timer.

:::{note}
Python also provides in the library `time` the function `time.sleep(...)`.
in the library.

However, you should **not** use this function, because the global
delay can lead to page effects.
:::

## Start a timer

You can start a timer like this:

``` python
from miniworldmaker import *

ActionTimer(24, player.move)
```

![UML](/_images/actiontimer.png)

The function receives 2 arguments:

* After **24** frames (1).
* ... the function `player.move` is executed (2).

## The different timers

There are different types of timers:

### ActionTimer

The ActionTimer calls a method with arguments after a specified time and then removes itself.
arguments and then removes itself.

``` python
import miniworldmaker as mwm

mwm.ActionTimer(24, player.move, None)
```

After 24 frames the timer is called and then executes once the function
`move` of the object `player` once.

### LoopActionTimer

The LoopActionTimer does the same as the action timer, but the action is
the action is repeated over and over again with equal intervals.


This is how you create a loop action timer:

``` python
LoopActionTimer(24, player.move)
```

Every 24 frames the function `move` of the object `player` is called.

So you can remove a LoopActionTimer again:

``` python
import miniworldmaker as mwm
...
loopactiontimer = mwm.LoopActionTimer(24, player.move)
...
loopactiontimer.unregister()
```

The loopactiontimer is removed with this command.

## Get timer with events

Similar to the sensors, you can register methods for timers that react on
a timer event.

Such a method can look like this:

``` python
@timer(frames = 24)
def moving():
    player.move()
```

At frame 24 the method `moving` is called.

With a loop timer the function can be registered like this:

``` python
@loop(frames = 48)
def moving():
    player.turn_left()
    player.move(2)
```

Here the moving() function is repeated every 48 frames.


