import inspect


class MWMInspection:

    def __init__(self, generator):
        self.instance = generator

    def get_instance_method(self, name):
        """
        If a (token-)object has method this returns the method by a given name
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

    def has_parent_with_name(self, name):
        parents = self.instance__class__.__bases__
        for parent in parents:
            if parent.__name__ == name:
                return True
        return False

    def has_parent(self, parent_cls):
        parents = inspect.getmro(self.instance.__class__)
        for parent in parents:
            if parent == parent_cls:
                return True
        return False

    def has_class_name(self, name):
        if self.instance.__class__.__name__ == name:
            return True
        return False

    def bind_method(self, method):
        bound_method = method.__get__(self.instance, self.instance.__class__)
        setattr(self.instance, method.__name__, bound_method)
        if method.__name__ == "on_setup":
            self.instance.on_setup()
        return bound_method

    def get_and_call_method(self, name, args, errors=False):
        method = self.get_instance_method(name)
        if method:
            self.call_instance_method(method, args)
        elif errors:
            raise Exception("Method not found")

    def all_subclasses(cls):
        def rec_all_subs(base_cls) -> set:
            if cls.subclasses is None:
                return set(base_cls.__subclasses__()).union(
                    [s for c in base_cls.__subclasses__() for s in rec_all_subs(c)])
            else:
                return cls.subclasses

        return rec_all_subs(cls)