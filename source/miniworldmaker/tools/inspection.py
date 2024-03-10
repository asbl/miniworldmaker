import inspect
import types
import functools


class Inspection:

    def __init__(self, generator):
        self.instance = generator

    def get_instance_method(self, name):
        """If a (token-)object has method this returns the method by a given name
        """
        if hasattr(self.instance, name):
            if callable(getattr(self.instance, name)):
                _method = getattr(self.instance, name)
                _bound_method = _method.__get__(self.instance, self.instance.__class__)
                return _bound_method
            else:
                return None
        else:
            return None

    def bind_method(self, method, name=None):
        bound_method = method.__get__(self.instance, self.instance.__class__)
        if name is None:
            setattr(self.instance, method.__name__, bound_method)
        else:
            setattr(self.instance, name, bound_method)
        return bound_method


    def unbind_method(self, method):
        delattr(self.instance, method.__name__, method)

    def get_and_call_method(self, name, args, errors=False):
        method = self.get_instance_method(name)
        if method:
            self.call_instance_method(method, args)
        elif errors:
            raise Exception("Method not found")
