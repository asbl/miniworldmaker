import math

import pygame
from boards import board_position
from tokens import board_connector
from tokens import token


class TiledBoardConnector(board_connector.BoardConnector):

    def __init__(self, token, board):
        super().__init__(token, board)
        self.token.size = (self.board.tile_size, self.board.tile_size)
        if hasattr(self, "is_static") and self.is_static is True:
            self.board.static_tokens_dict[token.position].append(token)
        else:
            self.board.dynamic_tokens.append(token)
        if token.size == (0, 0):
            token.size = (self.board.tile_size, self.board.tile_size)
        self.token.fps = token.board.default_token_speed

    def on_board(self, distance):
        target = self.get_destination(self.token.position, self.token.direction, distance)

    def get_destination(self, start, direction, distance) -> board_position.BoardPosition:
        x = start[0] + round(math.sin(math.radians(direction)) * distance)
        y = start[1] - round(math.cos(math.radians(direction)) * distance)
        return board_position.BoardPosition(x, y)

    def get_token_rect(self):
        _rect = pygame.Rect(0, 0, self.board.tile_size, self.board.tile_size)
        x = self.token.position[0] * (self.board.tile_size + self.board.tile_margin)
        y = self.token.position[1] * (self.board.tile_size + self.board.tile_margin)
        _rect.topleft = (x, y)
        return _rect

    def sensing_on_board(self, distance=0) -> bool:
        target = self.get_destination(self.token.position, self.token.direction, distance)
        on_board = target.is_on_board()
        return on_board

    def sensing_borders(self, distance = 0):
        target = self.get_destination(self.token.position, self.token.direction, distance)
        return target.borders()

    def sensing_tokens(self, distance: int = 1, token_type=None, exact=False) -> list:
        target = self.get_destination(self.token.position, self.token.direction, distance)
        self._update_token_positions()
        token_list = []
        if target.is_on_board():
            position = target
            if self.board.dynamic_tokens_dict[position.x, position.y]:
                token_list.extend(self.board.dynamic_tokens_dict[(position.x, position.y)])
            if self.board.static_tokens_dict[position.x, position.y]:
                token_list.extend(self.board.static_tokens_dict[(position.x, position.y)])
        token_list = [token for token in token_list if token != self.token]
        # Filter by token type
        if token_type is not None:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
        return token_list

    def sensing_token(self, distance: int = 1, token_type=None, exact=False) -> list:
        target = self.get_destination(self.token.position, self.token.direction, distance)
        self._update_token_positions()
        token_list = []
        if self.board.on_board(self.token.rect):
            position = self.token.position
            if self.board.dynamic_tokens_dict[position.x, position.y]:
                token_list.extend(self.board.dynamic_tokens_dict[(position.x, position.y)])
            if self.board.static_tokens_dict[position.x, position.y]:
                token_list.extend(self.board.static_tokens_dict[(position.x, position.y)])
        token_list = [token for token in token_list if token != self.token]
        # Filter by token type
        if token_type is not None:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
        if token_list:
            return token_list[0]

    def remove_from_board(self) -> None:
        if self.token in self.board.dynamic_tokens:
            self.board.dynamic_tokens.remove(self.token)
        if self.token in self.board.static_tokens_dict[self.token.position.to_tuple()]:
            self.board.static_tokens_dict[self.token.position.to_tuple()].remove(self.token)
        super().remove_from_board()

    def update_token(self, attribute, value):
        if attribute == "is_static" and value is True:
            self.board.static_tokens_dict[(self.token.x(), self.token.y())].append(token)
            if token in self.board.dynamic_tokens_dict:
                self.board.dynamic_tokens_dict.pop(token)
        else:
            self.board.dynamic_tokens.append(token)

    def _update_token_positions(self) -> None:
        self.board.dynamic_tokens_dict.clear()
        for token in self.board.dynamic_tokens:
            x, y = token.position[0], token.position[1]
            self.board.dynamic_tokens_dict[(x, y)].append(token)