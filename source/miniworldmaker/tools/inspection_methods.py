from typing import Union, Optional, Type
import inspect
from inspect import signature
from collections import defaultdict
from miniworldmaker.exceptions.miniworldmaker_exception import FirstArgumentShouldBeSelfError, NotCallableError, WrongArgumentsError, NotNullError, TokenClassNotFound
from miniworldmaker.tokens import token
import miniworldmaker


class InspectionMethods:

    token_class_ids = defaultdict()  # class_name -> id
    token_classes = defaultdict()  # class_name as string -> class
    token_class_id_counter = 0

    def __init__(self, generator):
        """Inspects a token or a token class

        Args:
            generator: A instance of token or a token class
        """
        if not inspect.isclass(generator):
            self.instance = generator
            self.token_class = generator.__class__
        else:
            self.token_class = generator

    @staticmethod
    def has_parent_with_name(instance, name):
        parents = instance.__class__.__bases__
        for parent in parents:
            if parent.__name__ == name:
                return True
        return False

    @staticmethod
    def has_parent(instance, cls):
        parents = inspect.getmro(instance.__class__)
        for parent in parents:
            if parent == cls:
                return True
        return False

    @staticmethod
    def has_class_name(instance, name):
        if instance.__class__.__name__ == name:
            return True
        return False

    @staticmethod
    def get_instance_method(instance, name):
        """
        If a (token-)object has method this returns the method by a given name
        """
        if hasattr(instance, name):
            if callable(getattr(instance, name)):
                _method = getattr(instance, name)
                _bound_method = _method.__get__(instance, instance.__class__)
                return _bound_method
            else:
                return None
        else:
            return None

    @staticmethod
    def get_class_methods_starting_with(cls, string):
        methods = [method for method in dir(cls) if
                   callable(getattr(cls, method)) and
                   method.startswith(string)]
        return methods

    @staticmethod
    def get_and_call_instance_method(instance, name, args, errors=False):
        method = InspectionMethods.get_instance_method(instance, name)
        if method:
            InspectionMethods.call_instance_method(instance, method, args)
        elif errors:
            raise Exception("Method not found")

    def get_and_call_method(self, name, args, errors=False):
        return InspectionMethods.get_and_call_instance_method(self.instance, name, args, errors)
    
    @staticmethod
    def call_instance_method(instance, method: callable, args: Optional[Union[tuple, list]], allow_none=True):
        # Don't call method if tokens are already removed:
        method = getattr(instance, method.__name__)
        if issubclass(instance.__class__, token.Token) and not instance.board:
            return
        InspectionMethods.check_signature(method, args, allow_none)
        if args == None:
            method()
        else:
            method(*args)
            
    @staticmethod
    def get_signature(method: callable, arguments: tuple, allow_none=True):
        InspectionMethods.check_signature(method, arguments, allow_none)
        return signature(method)

    @staticmethod
    def check_signature(method: callable, arguments: tuple, allow_none=False):
        if not type(callable(method)):
            raise NotCallableError(method)
        if arguments is None and not allow_none:
            raise NotNullError(method)
        if type(arguments) is not list and type(arguments) is not tuple and type(arguments) is not dict:
            arguments = [arguments]
        try:
            sig = signature(method)
        except ValueError:
            raise FirstArgumentShouldBeSelfError(method)
        i = 0
        for key, param in sig.parameters.items():
            if param.default == param.empty and i >= len(arguments):
                raise WrongArgumentsError(method, arguments)
            i = i + 1

    @staticmethod
    def call_method(method: callable, arguments: tuple, allow_none=True):
        InspectionMethods.check_signature(method, arguments, allow_none=True)
        if arguments == None:
            method()
        else:
            method(*arguments)

    @staticmethod
    def inherits_from(child, parent):
        if inspect.isclass(child):
            if parent.__name__ in [c.__name__ for c in inspect.getmro(child)] or parent.__name__ == child.__name__:
                return True
        return False

    def find_token_class_by_classname(self, classname: str) -> Union[None, Type["miniworldmaker.Token"]]:
        classname = classname.lower()
        for token_cls in self.get_all_token_classes():
            if token_cls.__name__.lower() == classname:
                return token_cls
        return None

    def get_token_parent_class(self):
        """Gets the class miniworldmaker.Token class for a specific token subclass. 

        This is needed, so you can find all miniworldmaker token subclasses at runtime.
        """
        for tokencls in inspect.getmro(self.token_class):
            if tokencls == miniworldmaker.Token or tokencls == token.Token:
                return tokencls

    @staticmethod
    def get_subclasses_for_cls(token_cls):
        def all_subclasses(cls):
            return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])
        token_set = set()
        token_set.add(token_cls)
        return token_set.union(all_subclasses(token_cls))

    def get_subclasses(self) -> set:
        """Returns the token class and all parent classes of token. 

        Returns:
            Set with all token classes and parent classes
        """
        return InspectionMethods.get_subclasses_for_cls(self.token_class)

    def get_all_token_classes(self):
        token_parent_class = self.get_token_parent_class()
        return InspectionMethods.get_subclasses_for_cls(token_parent_class)
