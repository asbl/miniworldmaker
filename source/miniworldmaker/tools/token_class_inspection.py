import inspect
from typing import Union, Type

import miniworldmaker.tokens.token as token
from miniworldmaker.boards import board_base as board_base


class TokenClassInspection:

    def __init__(self, generator):
        """Inspects a token or a token class

        Args:
            generator: A instance of token or a token class
        """
        if not inspect.isclass(generator):
            if isinstance(generator, board_base.BaseBoard):
                self.instance = generator.tokens.get_sprite(0)
                self.token_class = generator.tokens.get_sprite(0).__class__
            else:
                self.instance = generator
                self.token_class = generator.__class__
        else:
            self.token_class = generator

    def get_class_methods_starting_with(self, string):
        methods = [method for method in dir(self.token_class) if
                   callable(getattr(self.token_class, method)) and
                   method.startswith(string)]
        return methods

    @staticmethod
    def get_all_token_classes():
        token_parent_class = token.Token
        return TokenClassInspection(token_parent_class).get_subclasses_for_cls()

    def get_token_parent_class(self):
        return token.Token

    def get_subclasses_for_cls(self):
        def all_subclasses(cls):
            return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])

        token_set = set()
        token_set.add(self.token_class)
        return token_set.union(all_subclasses(self.token_class))

    def find_token_class_by_classname(self, class_name: str) -> Union[None, Type["token.Token"]]:
        class_name = class_name.lower()
        for token_cls in self.get_all_token_classes():
            if token_cls.__name__.lower() == class_name:
                return token_cls
        return None