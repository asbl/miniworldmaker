from miniworldmaker.base import app
from miniworldmaker.tools import method_caller


class Timed():
    """Base class for all timers
    """

    def __init__(self):
        self.board = app.App.running_board
        self.board.timed_objects.append(self)
        self.running = True

    def tick(self):
        self.time = self.time - 1

    def unregister(self):
        """remove timer from board
        """
        if self in self.board.timed_objects:
            self.board.timed_objects.remove(self)
        del (self)


class Timer(Timed):
    """Base class for timers. Calls act() Method after `time` frames.
    """

    def __init__(self, time: int):
        super().__init__()
        self.time = time
        self.actual_time = 0

    def tick(self):
        self.actual_time += 1
        if self.actual_time % self.time == 0:
            self.act()

    def act(self):
        """Act method for timer. Called after `actual_time` frames.
        """
        pass


class ActionTimer(Timer):
    """Calls a method after `time` frames.

    Example:
        Player moves after 48 frames::

            miniworldmaker.ActionTimer(48, player.move, 2)

        Same as above with decorator::

            @miniworldmaker.timer(frames = 24)
            def moving():
                player.move()
    """

    def __init__(self, time: int, method: callable, arguments=None):
        """

        Args:
            time (int): After `time` frames, the method is called
            method (callable): The method to call.
            arguments ([type], optional): Arguments for the method.
        """
        super().__init__(time)
        self.method: callable = method
        if arguments or arguments == 0:
            self.arguments = [arguments]
        else:
            self.arguments = None

    def act(self):
        self._call_method()
        self.unregister()
        
    def _call_method(self):
        method_caller.call_method(self.method, self.arguments, allow_none=False)


class LoopActionTimer(ActionTimer):
    """Calls a method after `time` frames repeatedly until the timer is unregistered.
    
    Example:
        Player moves after 48 frames::

            miniworldmaker.LoopTimer(48, player.move, 2)

        Same as above with decorator::

            @miniworldmaker.loop(frames = 24)
            def moving():
                player.move()
    """

    def act(self):
        self._call_method()


def timer(*args, **kwargs):
    """Used as decorator for timed actions.

    Example::

        @miniworldmaker.timer(frames = 24)
            def moving():
                player.move()
    """

    def inner(method):
        timer = ActionTimer(kwargs["frames"], method)
        return timer

    return inner


def loop(*args, **kwargs):
    """Used as decorator for looped actions.

    Example::

        @miniworldmaker.loop(frames = 24)
            def moving():
                player.move()
    """

    def inner(method):
        timer = LoopActionTimer(kwargs["frames"], method)
        return timer

    return inner
