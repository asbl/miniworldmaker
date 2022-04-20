from typing import List, Union

import miniworldmaker.boards.board as board
import miniworldmaker.tokens.token as token
import miniworldmaker.tools.token_class_inspection as token_class_inspection
from miniworldmaker.exceptions.miniworldmaker_exception import NotImplementedOrRegisteredError


class TokenBoardSensor():

    def __init__(self, token: "token.Token", board: "board.Board"):
        super().__init__()
        self.token : "token.Token" = token
        self.board : "board.Board" = board

    def remove_from_board(self):
        """Removes a token from board
        """
        self.board.tokens.remove(self.token)
        self.token.board = None

    def self_remove(self):
        """
        Method is overwritten in subclasses
        """
        pass

    def filter_token_list(self, token_list: Union[List["token.Token"], None], token_filter) -> List["token.Token"]:
        # if token_list is None, return empty lsit
        if token_list == None:
            return []
        # Filter tokens by classname
        if type(token_filter) == str:
            token_list = self.filter_tokens_by_classname(token_list, token_filter)
        # if
        if token_class_inspection.TokenClassInspection.inherits_from(token_filter.__class__, token.Token):
            token_list = self.filter_tokens_by_instance(token_list, token_filter)
        return token_list

    def filter_tokens_by_classname(self, token_list : List["token.Token"], token_filter: str) -> List["token.Token"]:
        token_type = token_class_inspection.TokenClassInspection(self.token).find_token_class_by_classname(token_filter)
        if token_type == None:
            return token_list
        if token_type:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
            return token_list
        else:
            return token_list

    def filter_tokens_by_instance(self, token_list : List["token.Token"], token_filter):
        for token in token_list:
            if token == token_filter:
                return [token]
        return []

    def remove_self_from_token_list(self, token_list : List["token.Token"]):
        if token_list and self.token in token_list:
            token_list.remove(self.token)
        return token_list

    def sensing_token(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()

    def sensing_tokens(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()

