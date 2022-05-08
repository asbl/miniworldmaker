import inspect
from collections import defaultdict
from inspect import signature
from typing import Union, Optional

from miniworldmaker.exceptions.miniworldmaker_exception import FirstArgumentShouldBeSelfError, NotCallableError, \
    WrongArgumentsError, NotNullError
from miniworldmaker.tokens import token


class InspectionMethods:
    token_class_ids = defaultdict()  # class_name -> id
    token_classes = defaultdict()  # class_name as string -> class
    token_class_id_counter = 0

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
