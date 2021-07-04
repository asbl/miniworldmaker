import inspect
from inspect import signature

from miniworldmaker.app import app

class Timed():
    def __init__(self):
        self.board = app.App.board
        self.board.timed_objects.append(self)
        self.running = True

    def tick(self):
        self.time = self.time - 1

    def unregister(self):
        if self in self.board.timed_objects:
            self.board.timed_objects.remove(self)
        del(self)



class Timer(Timed):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.actual_time = 0

    def tick(self):
        self.actual_time += 1
        if self.actual_time % self.time == 0:
            self.act()

    def act(self):
        pass


class ZeroTimer(Timed):
    def __init__(self, time):
        super().__init__()
        self.time = time

    def tick(self):
        self.time -= 1
        if self.time == 0:
            self.act()
            self.unregister()

    def act(self):
        pass

class CallTimer(Timer):
    def __init__(self, time, method, arguments = None):
        super().__init__(time)
        self.method = method
        self.arguments = arguments    

    def _call_method(self):
        sig = signature(self.method)
        if type(self.arguments) == list:
            if len(sig.arguments) == len(self.arguments):
                self.method(*self.arguments)
            else:
                info = inspect.getframeinfo(inspect.currentframe())
                raise Exception(
                    "Wrong number of arguments for " + str(self.method) + " in , got " + str(
                        len(self.arguments)) + " but should be " + str(
                        len(sig.arguments)) +
                    "Additional Information: File:" + str(info.filename), "; Method: " + str(method)
                )
        else:
            if self.arguments is None:
                self.method()
            else:
                self.method(self.arguments)

class ActionTimer(CallTimer):

    def __init__(self, time, method, arguments = None):
        super().__init__(time, method, arguments)

    def act(self):
        self._call_method()
        self.unregister()
        self.success()

    def success(self, method = None, arguments = None):
        if method is not None and arguments is None:
            method()
        if method is not None and arguments is not None:
            method(arguments)



class LoopActionTimer(CallTimer):

    def __init__(self, time, method, arguments = None):
        super().__init__(time, method, arguments)

    def act(self):
        self._call_method()


"@decorator"
def timer(*args, **kwargs):
    def inner(method):
        timer = ActionTimer(kwargs["frames"], method)
    return inner

"@decorator"
def loop(*args, **kwargs):
    def inner(method):
        timer = LoopActionTimer(kwargs["frames"], method)
    return inner