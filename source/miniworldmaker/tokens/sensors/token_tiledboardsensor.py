import math

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.boards.tiled_board as board_module
import miniworldmaker.tokens.sensors.token_boardsensor as boardsensor
import miniworldmaker.tokens.token as token_module


class TokenTiledBoardSensor(boardsensor.TokenBoardSensor):
    """
    The TiledBoardConnector connects a token to a tiled_board
    """

    def __init__(self, token: "token_module.Token", board: "board_module.TiledBoard"):
        super().__init__(token, board)
        self.board = board
        self.token.fps = token.board.default_token_speed

    @staticmethod
    def get_destination(start, direction, distance) -> "board_position.Position":
        x = start[0] + round(math.sin(math.radians(direction)) * distance)
        y = start[1] - round(math.cos(math.radians(direction)) * distance)
        return board_position.Position(x, y)

    def sensing_on_board(self, distance=0) -> bool:
        """
        Checks if token is on board

        Args:
            distance: If distance > 0, it will be checked, if the token is on the board if moved two steps forward

        Returns: True if token is on board.

        """
        target = self.get_destination(self.token.position, self.token.direction, distance)
        on_board = self.is_position_on_board(target)
        return on_board

    def sensing_borders(self, distance=0):
        """
        Checks if token is touching borders

        Args:
            distance: If distance > 0, it will be checked, if the token is touching borders, if moved two steps forward

        Returns: A List of touched borders, e.g. ["left", "top"]

        """
        target = self.get_destination(self.token.position, self.token.direction, distance)
        rect = (target.x, target.y, self.board.tile_size, self.board.tile_size)
        return self.token.board.position_manager.get_borders_from_rect(rect)

    def sensing_tokens(self, token_filter=None) -> list:
        """
        Senses tokens at current position

        Args:
            distance: If distance > 0, it will be checked, if the token is touching other tokens,
            if moved two steps forward
            token_filter: Filters by token_type. token_type is a Class of token.

        Returns: A list of tokens at token position

        """
        target_position = self.token.position
        token_list: list = list()
        if self.is_position_on_board(target_position):
            token_list = self.board.sensing_tokens(target_position)
        if not token_list:
            token_list = []
        token_list = self.remove_self_from_token_list(token_list)
        token_list = self.filter_token_list(token_list, token_filter)
        return token_list

    def sensing_token(self, token_filter=None) -> "token_module.Token":
        """
        Senses tokens at current position. The method is faster than sensing_tokens.

        Args:
            distance: If distance > 0, it will be checked, if the token is touching other tokens,
            if moved two steps forward
            token_filter: Filters by token_type. token_type is a Class of token.

        Returns: The first token at current position or None.

        """
        token_list = self.sensing_tokens(token_filter=token_filter)
        token_list = self.remove_self_from_token_list(token_list)
        token_list = self.filter_token_list(token_list, token_filter)
        if token_list:
            return token_list[0]

    def remove_from_board(self) -> None:
        """
        Removes a token from board
        """
        if self.token in self.board.dynamic_tokens:
            self.board.dynamic_tokens.remove(self.token)
        if self.token in self.board.static_tokens_dict[self.token.position]:
            self.board.static_tokens_dict[self.token.position.to_tuple()].remove(self.token)
        super().remove_from_board()

    def self_remove(self):
        self.remove_from_board()

    def sensing_point(self, pixel_position):
        return self.token.position == self.board.get_from_pixel(pixel_position)

    def sense_color_at(self, direction: int = 0, distance: int = 1) -> list:
        if direction == 0:
            direction = self.token.direction
        destination = self.get_destination(self.token.position, direction, distance)
        destination = self.board.to_pixel(destination)
        return self.board.background.get_color(destination)