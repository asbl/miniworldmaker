import math
from abc import ABC
from typing import List, Union, Type

import miniworldmaker.positions.position as board_position
import miniworldmaker.positions.rect as board_rect
import miniworldmaker.tools.token_class_inspection as token_class_inspection
from miniworldmaker.boards.board_templates.pixel_board import board as board_mod
from miniworldmaker.exceptions.miniworldmaker_exception import NotImplementedOrRegisteredError
from miniworldmaker.tokens import token as token_mod


class TokenBoardSensor(ABC):
    def __init__(self, token: "token_mod.Token", board: "board_mod.Board"):
        super().__init__()
        self.token: "token_mod.Token" = token

    @property
    def board(self):
        return self.token.board

    def remove_from_board(self):
        """Removes a token from board"""
        self.board.tokens.remove(self.token)
        self.token.board = None

    def self_remove(self):
        """
        Method is overwritten in subclasses
        """
        pass

    def filter_tokens(self, detected_tokens, token_filter: list):
        """
        Filters a list of tokens
        :param detected_tokens: a list of tokens
        :param token_filter: list of token filters
        :return:
        """
        if detected_tokens:
            detected_tokens = self._filter_token_list(detected_tokens, token_filter)
        if detected_tokens and len(detected_tokens) >= 1:
            return detected_tokens
        else:
            return []

    def filter_first_token(self, detected_tokens: list, token_filter):
        if detected_tokens:
            detected_tokens = self._filter_token_list(detected_tokens, token_filter)
        if detected_tokens and len(detected_tokens) >= 1:
            rvalue = detected_tokens[0]
            del detected_tokens
            return rvalue
        else:
            return []

    def _filter_token_list(
            self, token_list: Union[List["token_mod.Token"], None],
            token_filter: Union[str, "token_mod.Token", Type["token_mod.Token"]]
    ) -> List["token_mod.Token"]:
        # if token_list is None, return empty list
        if token_list is None:
            return []
        # Filter tokens by class name
        if not token_filter:
            return token_list
        if type(token_filter) == str:
            token_list = self._filter_tokens_by_classname(token_list, token_filter)
        elif isinstance(token_filter, token_mod.Token):
            token_list = self._filter_tokens_by_instance(token_list, token_filter)
        elif issubclass(token_filter, token_mod.Token):
            token_list = self._filter_tokens_by_class(token_list, token_filter)
        return token_list

    def _filter_tokens_by_class(
            self, token_list: List["token_mod.Token"], token_filter: Union[Type["token_mod.Token"], None]
    ) -> List["token_mod.Token"]:
        if token_filter is None:
            return token_list
        if token_filter:
            token_list = [token for token in token_list if
                          token.__class__ == token_filter or issubclass(token.__class__, token_filter)]
            return token_list
        else:
            return token_list

    def _filter_tokens_by_classname(
            self, token_list: List["token_mod.Token"], token_filter: str
    ) -> List["token_mod.Token"]:
        token_type = token_class_inspection.TokenClassInspection(self.token).find_token_class_by_classname(
            token_filter
        )
        return self._filter_tokens_by_class(token_list, token_type)

    @staticmethod
    def _filter_tokens_by_instance(token_list: List["token_mod.Token"], token_filter):
        for token in token_list:
            if token == token_filter:
                return [token]
        return []

    def _remove_self_from_token_list(self, token_list: List["token_mod.Token"]):
        if token_list and self.token in token_list:
            token_list.remove(self.token)
        return token_list

    def detect_token(self, token_filter) -> Union["token_mod.Token", None]:
        raise NotImplementedOrRegisteredError(self.detect_token)

    def detect_tokens(self, token_filter) -> List["token_mod.Token"]:
        raise NotImplementedOrRegisteredError(self.detect_tokens)

    def detect_point(self, pixel_position) -> bool:
        return self.token.position_manager.get_global_world_rect().collidepoint(pixel_position)

    def detect_rect(self, rect):
        return self.token.position_manager.get_global_world_rect().colliderect(rect)

    def is_token_on_the_board(self, distance: int) -> bool:
        raise NotImplementedOrRegisteredError(self.is_token_on_the_board)

    def detect_borders(self, distance: int) -> list:
        raise NotImplementedOrRegisteredError(self.detect_borders)

    def detect_color(self, source: Union[tuple, list]) -> bool:
        return self.detect_color_at(0, 0) == source

    def detect_colors(self, source: list) -> bool:
        for color in source:
            if self.detect_color_at(0, 0) == color:
                return True
        return False

    def detect_tokens_at(self, token_filter=None, direction: int = 0, distance: int = 1) -> list:
        if direction is None:
            direction = self.token.direction
        destination = self.get_token_destination(self.token, direction, distance)
        detected_tokens = self.board.get_tokens_at_position(destination)
        return self.filter_tokens(detected_tokens, token_filter)

    def detect_color_at(self, direction: int = 0, distance: int = 1) -> tuple:
        if direction is None:
            direction = self.token.direction
        destination = self.get_token_destination(self.token.center, direction, distance)
        return self.board.background.get_color(destination)

    @classmethod
    def get_token_destination(cls, token: "tkn.Token", direction: float, distance: float) -> "board_position.Position":
        return cls.get_destination(token.position, direction, distance)

    @staticmethod
    def get_destination(start, direction, distance) -> "board_position.Position":
        exact_position_x = start[0] + math.sin(math.radians(direction)) * distance
        exact_position_y = start[1] - math.cos(math.radians(direction)) * distance
        pos = board_position.Position.create((exact_position_x, exact_position_y))
        return pos

    def get_borders_from_rect(self, rect):
        """
        Gets all borders the rect ist touching.

        Returns: A list of borders as strings: "left", "bottom", "right", or "top"

        """
        rect = board_rect.Rect.create(rect)
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.board.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.board.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def get_color(self, position):
        """ Returns the board-color at the current board-position

        Returns: The board-color at the current board position as tuple
        with r,g,b value and transparency (e.g. (255, 0, 0, 100)
        """
        position = board_position.BoardPosition.create(position)
        if self.board.contains_position(position):
            return self.board.background.get_color_from_pixel(position)
        else:
            return ()

    def get_distance_to(self, obj: Union["token_mod.Token", "board_position.Position", tuple]) -> float:
        """ Implemented in subclasses
        """
        pass
