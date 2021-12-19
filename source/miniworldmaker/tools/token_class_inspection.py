import inspect
import miniworldmaker
from miniworldmaker.boards import board
from miniworldmaker.tokens import token
from typing import Union, Type

class TokenClassInspection:

    def __init__(self, generator):
        """Inspects a token or a token class

        Args:
            generator: A instance of token or a token class
        """
        if not inspect.isclass(generator):
            if isinstance(generator, miniworldmaker.Board) or isinstance(generator, board.Board):
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

    def get_all_token_classes(self):
        token_parent_class = self.get_token_parent_class() # get miniworldmaker.Token
        return TokenClassInspection(token_parent_class).get_subclasses_for_cls()

    def get_token_parent_class(self):
        """Gets the class miniworldmaker.Token class for a specific token subclass. 

        This is needed, so you can find all miniworldmaker token subclasses at runtime.
        """
        for tokencls in inspect.getmro(self.token_class):
            if tokencls == miniworldmaker.Token or tokencls == token.Token:
                return tokencls

    def get_subclasses_for_cls(self):
        def all_subclasses(cls):
            return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])
        token_set = set()
        token_set.add(self.token_class)
        return token_set.union(all_subclasses(self.token_class))

    def find_token_class_by_classname(self, classname: str) -> Union[None, Type["miniworldmaker.Token"]]:
        classname = classname.lower()
        for token_cls in self.get_all_token_classes():
            if token_cls.__name__.lower() == classname:
                return token_cls
        return None

    @staticmethod
    def inherits_from(child, parent):
        if inspect.isclass(child):
            if parent.__name__ in [c.__name__ for c in inspect.getmro(child)] or parent.__name__ == child.__name__:
                return True
        return False