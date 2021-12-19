import math
import inspect
from typing import List
import miniworldmaker
from typing import Union
from miniworldmaker.tokens import token
from miniworldmaker.tools import token_class_inspection
from miniworldmaker.tools import token_inspection
from miniworldmaker.exceptions.miniworldmaker_exception import NotImplementedOrRegisteredError


class TokenBoardSensor():

    def __init__(self, token: "miniworldmaker.Token", board: "miniworldmaker.Board"):
        super().__init__()
        self.token : "miniworldmaker.Token" = token
        self.board : "miniworldmaker.Board" = board

    def remove_from_board(self):
        """Removes a token from board
        """
        self.board.tokens.remove(self.token)
        self.token.board = None

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.center
        x = (destination[0] - pos[0])
        y = (destination[1] - pos[1])
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                self.token.direction = (math.degrees(math.atan(m)) - 90)
            else:
                # destination is right
                self.token.direction = (math.degrees(math.atan(m)) + 90)
            return self.token.direction
        else:
            m = 0
            if destination[1] > self.token.position[1]:
                self.token.direction = 180
                return self.token.direction
            else:
                self.token.direction = 0
                return self.token.direction

    def remove(self):
        """
        Method is overwritten in subclasses
        """
        pass

    def filter_token_list(self, token_list: Union[List["miniworldmaker.Token"], None], token_filter) -> List["miniworldmaker.Token"]:
        # if token_list is None, return empty lsit
        if token_list == None:
            return []
        # Filter tokens by classname
        if type(token_filter) == str:
            self.filter_tokens_by_classname(token_list, token_filter)
        # if
        if token_class_inspection.TokenClassInspection.inherits_from(token_filter.__class__, token.Token):
            self.filter_tokens_by_instance(token_list, token_filter)
        return token_list

    def filter_tokens_by_classname(self, token_list : List["miniworldmaker.Token"], token_filter: str) -> List["miniworldmaker.Token"]:
        token_type = token_class_inspection.TokenClassInspection(self.token).find_token_class_by_classname(token_filter)
        if token_type == None:
            return token_list
        if token_type:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
            return token_list
        else:
            return token_list

    def filter_tokens_by_instance(self, token_list : List["miniworldmaker.Token"], token_filter):
        for token in token_list:
            if token == token_filter:
                return [token]
        return []

    def remove_self_from_token_list(self, token_list : List["miniworldmaker.Token"]):
        if token_list and self.token in token_list:
            token_list.remove(self.token)
        return token_list

    def sensing_token(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()

    def sensing_tokens(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()
