import math
from typing import List, Union, Type

import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_rect as board_rect
import miniworldmaker.boards.board as board_mod
import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tools.token_class_inspection as token_class_inspection
from miniworldmaker.exceptions.miniworldmaker_exception import NotImplementedOrRegisteredError


class TokenBoardSensor:
    def __init__(self, token: "token_mod.Token", board: "board_mod.Board"):
        super().__init__()
        self.token: "token_mod.Token" = token
        self.board: "board_mod.Board" = board

    def remove_from_board(self):
        """Removes a token from board"""
        self.board.tokens.remove(self.token)
        self.token.board = None

    def self_remove(self):
        """
        Method is overwritten in subclasses
        """
        pass

    def filter_token_list(
        self, token_list: Union[List["token_mod.Token"], None], token_filter : Union[str, "token_mod.Token", Type["token_mod.Token"] ]
    ) -> List["token_mod.Token"]:
        # if token_list is None, return empty list
        if token_list is None:
            return []
        # Filter tokens by class name
        if not token_filter:
            return token_list
        if type(token_filter) == str:
            token_list = self.filter_tokens_by_classname(token_list, token_filter)
        elif isinstance(token_mod.Token, token_filter):
            token_list = self.filter_tokens_by_instance(token_list, token_filter)
        elif issubclass(token_mod.Token, token_filter):
            token_list = self.filter_tokens_by_class(token_list, token_filter)
        return token_list

    def filter_tokens_by_class(
        self, token_list: List["token_mod.Token"], token_filter: Union[Type["token_mod.Token"], None]
    ) -> List["token_mod.Token"]:
        if token_filter is None:
            return token_list
        if token_filter:
            token_list = [token for token in token_list if issubclass(token.__class__, token_filter)]
            return token_list
        else:
            return token_list
        
    def filter_tokens_by_classname(
        self, token_list: List["token_mod.Token"], token_filter: str
    ) -> List["token_mod.Token"]:
        token_type = token_class_inspection.TokenClassInspection(self.token).find_token_class_by_classname(
            token_filter
        )
        return self.filter_tokens_by_class(token_list, token_type)

    @staticmethod
    def filter_tokens_by_instance(token_list: List["token_mod.Token"], token_filter):
        for token in token_list:
            if token == token_filter:
                return [token]
        return []

    def remove_self_from_token_list(self, token_list: List["token_mod.Token"]):
        if token_list and self.token in token_list:
            token_list.remove(self.token)
        return token_list

    def sensing_token(self, token_filter=None) -> Union["token_mod.Token", None]:
        raise NotImplementedOrRegisteredError(self.sensing_token)

    def sensing_tokens(self, token_filter=None) -> List["token_mod.Token"]:
        raise NotImplementedOrRegisteredError(self.sensing_tokens)

    def sensing_point(self, pixel_position):
        return self.token.rect.collidepoint(pixel_position)

    def sensing_rect(self, rect):
        return self.token.rect.colliderect(rect)

    def sensing_on_board(self, distance: int) -> bool:
        raise NotImplementedOrRegisteredError(self.sensing_on_board)

    def sensing_borders(self, distance: int) -> list:
        raise NotImplementedOrRegisteredError(self.sensing_borders)

    def sensing_color(self, color: tuple) -> bool:
        return self.sense_color_at(0, 0) == color

    def sensing_tokens_at(self, direction: int = 0, distance: int = 1) -> list:
        if direction == 0:
            direction = self.token.direction
        destination = self.get_destination(self.token.center, direction, distance)
        return self.get_tokens_at_position(destination)

    def sense_color_at(self, direction: int = 0, distance: int = 1) -> tuple:
        if direction == 0:
            direction = self.token.direction
        destination = self.get_destination(self.token.center, direction, distance)
        return self.board.background.get_color(destination)

    @staticmethod
    def get_destination(start, direction, distance) -> "board_position.Position":
        exact_position_x = start[0] + math.sin(math.radians(direction)) * distance
        exact_position_y = start[1] - math.cos(math.radians(direction)) * distance
        pos = board_position.Position.create((exact_position_x, exact_position_y))
        return pos

    @staticmethod
    def is_position_on_board(pos):
        """
        Checks if Position is on board

        Returns:
            True, if Position is on board.
        """
        board = app.App.board
        if 0 <= pos[0] < board.columns and 0 <= pos[1] < board.rows:
            return True
        else:
            return False

    @classmethod
    def is_rect_completly_on_board(cls, rect):
        rect = board_rect.Rect.create(rect)
        topleft_on_board = cls.is_position_on_board(rect.topleft)
        bottom_right_on_board = TokenBoardSensor.is_position_on_board(rect.bottomright)
        return topleft_on_board or bottom_right_on_board

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
        """
        Returns the board-color at the current board-position

        Returns: The board-color at the current board position as tuple
        with r,g,b value and transparency (e.g. (255, 0, 0, 100)

        """
        position = board_position.BoardPosition.create(position)
        if self.is_position_on_board(position):
            return self.board.background.get_color_from_pixel(position)
        else:
            return ()
