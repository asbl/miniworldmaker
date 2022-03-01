# Timer

With **timers** you can execute events **time controlled**. If you
e.g. want an action to occur not immediately, but with a delay of some
milliseconds or seconds delay, you can use a timer.
timer.

``` {note}
Python also provides in the `time` library the function `time.sleep(...)`.
in the library.

However, you should **not** use this function, since the global
delay can lead to page effects.
```
## Start a timer

You can start a timer like this:

``` python
miniworldmaker.ActionTimer(24, player.move)
```

![UML](/_images/actiontimer.png)

The function receives 2 arguments:

- After **24** frames (1)
- \... the function `player.move` is executed (2).

## The different timers

There are different types of timers:

### ActionTimer

The ActionTimer calls a method with arguments after a specified time and then removes itself.
arguments and then removes itself.

``` python
miniworldmaker.ActionTimer(24, player.move, None)
```

### LoopActionTimer

The LoopActionTimer does the same thing as the action timer, but
the action is repeated again and again with equal intervals. If
this loop is to end, the timer must be deleted:

- How to create a loop action timer. The first parameter specifies
    in which intervals the loop should be repeated.

    ``` python
    loopactiontimer = miniworldmaker.LoopActionTimer(24, player.move)
    ```

- This is how you can remove a LoopActionTimer.

    ``` python
    loopactiontimer.unregister()
    ```
