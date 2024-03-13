from typing import Optional, Union, Callable

from miniworldmaker.tokens import token
from miniworldmaker.tools import method_caller
from miniworldmaker.tools import inspection


class TokenInspection(inspection.Inspection):

    def call_instance_method(self, method: Callable, args: Optional[Union[tuple, list]], allow_none=True):
        # Don't call method if tokens are already removed:
        method = getattr(self.instance, method.__name__)
        if issubclass(self.instance.__class__, token.Token) and not self.instance.board:
            return
        method_caller.check_signature(method, args, allow_none)
        if not args :
            method()
        else:
            method(*args)
