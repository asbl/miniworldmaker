import inspect
from typing import Optional, Union
from miniworldmaker.tokens import token
from miniworldmaker.tools.mwminspection import MWMInspection


class TokenInspection(MWMInspection):


    def call_instance_method(self, method: callable, args: Optional[Union[tuple, list]], allow_none=True):
        # Don't call method if tokens are already removed:
        method = getattr(self.instance, method.__name__)
        if issubclass(self.instance.__class__, token.Token) and not self.instance.board:
            return
        self.instance.check_signature(method, args, allow_none)
        if args == None:
            method()
        else:
            method(*args)