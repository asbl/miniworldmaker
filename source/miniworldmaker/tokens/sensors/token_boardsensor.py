from typing import List, Union

import miniworldmaker.boards.board as board
import miniworldmaker.tokens.token as token
import miniworldmaker.tools.token_class_inspection as token_class_inspection
import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_position as board_position
from miniworldmaker.exceptions.miniworldmaker_exception import NotImplementedOrRegisteredError
import miniworldmaker.board_positions.board_rect as board_rect


class TokenBoardSensor():

    def __init__(self, token: "token.Token", board: "board.Board"):
        super().__init__()
        self.token: "token.Token" = token
        self.board: "board.Board" = board

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

    def filter_tokens_by_classname(self, token_list: List["token.Token"], token_filter: str) -> List["token.Token"]:
        token_type = token_class_inspection.TokenClassInspection(self.token).find_token_class_by_classname(token_filter)
        if token_type == None:
            return token_list
        if token_type:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
            return token_list
        else:
            return token_list

    def filter_tokens_by_instance(self, token_list: List["token.Token"], token_filter):
        for token in token_list:
            if token == token_filter:
                return [token]
        return []

    def remove_self_from_token_list(self, token_list: List["token.Token"]):
        if token_list and self.token in token_list:
            token_list.remove(self.token)
        return token_list

    def sensing_token(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()

    def sensing_tokens(self, token_filter=None, distance: int = 0) -> Union["token.Token", None]:
        raise NotImplementedOrRegisteredError()

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
        board = app.App.board
        rect = board_rect.Rect.create(rect)
        topleft_on_board = cls.is_position_on_board(rect.topleft)
        bottom_right_on_board = TokenBoardSensor.is_position_on_board(rect.bottomright)
        return topleft_on_board or bottom_right_on_board

    def get_colors_in_rect(self, rect, rect_borders=None):
        colors = []
        rect = board_rect.Rect.create(rect)
        for x in range(self.width):
            if rect_borders is None or "left" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + x, rect.y))
                if color not in colors:
                    colors.append(color)
            if rect_borders is None or "right" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + x, rect.y + rect.height))
                if color not in colors:
                    colors.append(color)
        for y in range(self.height):
            if rect_borders is None or "top" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x, rect.y + y))
                if color not in colors:
                    colors.append(color)
            if rect_borders is None or "bottom" in rect_borders:
                color = self.board.background.get_color_from_pixel((rect.x + rect.width, rect.y + y))
                if color not in colors:
                    colors.append(color)
        return colors

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

    def sensing_point(self, pixel_position):
        return self.token.rect.collidepoint(pixel_position)

    def sensing_rect(self, rect):
        return self.token.rect.colliderect(rect)
