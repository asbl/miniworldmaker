from inspect import signature
from collections.abc import Iterable
from miniworldmaker.exceptions.miniworldmaker_exception import (
    FirstArgumentShouldBeSelfError,
    NotCallableError,
    WrongArgumentsError,
    NotNullError,
)
from typing import Optional


def get_signature(method: callable, arguments: tuple, allow_none=True):
    check_signature(method, arguments, allow_none)
    return signature(method)


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


def call_method(method: callable, arguments: Optional[tuple], allow_none=True):
    check_signature(method, arguments, allow_none=True)
    if arguments is None:
        method()
    else:
        if isinstance(arguments, Iterable):
            method(*arguments)
        else:
            method(arguments)
