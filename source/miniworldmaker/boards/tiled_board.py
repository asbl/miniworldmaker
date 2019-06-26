from collections import defaultdict
from typing import Union

import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.token import Token


class TiledBoard(Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=42, tile_margin=0):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            tile_size: The size of a tile
            tile_margin: The margin between tiles
        """
        self._dynamic_actors_dict = defaultdict(list)  # the dict is regularly updated
        self._dynamic_actors = []  # List with all dynamic actors
        self._static_tokens_dict = defaultdict(list)
        super().__init__(columns=columns, rows=rows, tile_size = tile_size, tile_margin = tile_margin)
        self.default_token_speed = 1
        self.set_size(columns, rows, tile_size, tile_margin)
        self.speed = 10

    def _update_token_positions(self) -> None:
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_tokens_at_position(self, position, token_type=None, exclude=None, singleitem = False) -> list:
        self._dynamic_actors_dict.clear()
        self._update_token_positions()
        token_list = []
        if self.is_position_on_board(self.rect):
            print(position.x, position.y, self._dynamic_actors_dict, self._static_tokens_dict)
            if self._dynamic_actors_dict[position.x, position.y]:
                token_list.extend(self._dynamic_actors_dict[(position.x, position.y)])
            if self._static_tokens_dict[position.x, position.y]:
                token_list.extend(self._static_tokens_dict[(position.x, position.y)])
        # Remove excluded
        if exclude in token_list:
            token_list.remove(exclude)
        # Filter by token type
        if token_type is not None:
            token_list = [token for token in token_list if issubclass(token.__class__, token_type)]
        if singleitem:
            if token_list:
                return token_list[0]
        else:
            return token_list

    def remove_from_board(self, token: Token) -> None:
        if token in self._dynamic_actors:
            self._dynamic_actors.remove(token)
        if token in self._static_tokens_dict[token.position.to_tuple()]:
            self._static_tokens_dict[token.position.to_tuple()].remove(token)
        super().remove_from_board(token)

    def remove_tokens_in_area(self, value: Union[pygame.Rect, tuple], actor_type=None) -> None:
        actors = self.get_tokens_in_area(value, actor_type)
        for actor in actors:
            self.remove_from_board(actor)

    def add_to_board(self, token: Token, position: Union[tuple, board_position.BoardPosition]) -> Token:
        if type(position) == board_position.BoardPosition:
            position = position.to_tuple()
        if hasattr(token, "is_static") and token.is_static is True:
            self._static_tokens_dict[position].append(token)
        else:
            self._dynamic_actors.append(token)
        if token.speed == 0:
            token.speed = self.default_token_speed
        super().add_to_board(token, position)
        if token.size == (0, 0):
            token.size = (self.tile_size, self.tile_size)
        token.dirty = 1
        return token

    def update_token(self, token: Token, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_tokens_dict[(token.x(), token.y())].append(token)
            if token in self._dynamic_actors_dict:
                self._dynamic_actors_dict.pop(token)
        else:
            self._dynamic_actors.append(token)

    @staticmethod
    def get_neighbour_cells(position: tuple) -> list:
        """Gets a list of all neighbour cells

        Args:
            position: the position

        Returns:
            a list of all neighbour cells

        """
        cells = []
        y_pos = position[0]
        x_pos = position[1]
        cells.append([x_pos + 1, y_pos])
        cells.append([x_pos + 1, y_pos + 1])
        cells.append([x_pos, y_pos + 1])
        cells.append([x_pos - 1, y_pos + 1])
        cells.append([x_pos - 1, y_pos])
        cells.append([x_pos - 1, y_pos - 1])
        cells.append([x_pos, y_pos - 1])
        cells.append([x_pos + 1, y_pos - 1])
        return cells

    def is_position_on_board(self, position: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> bool:
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        if type(position) == board_position.BoardPosition:
            position = position.to_rect()
        position = self.get_board_position_from_pixel(position.center)
        if position.x > self.columns - 1:
            return False
        elif position.y > self.rows - 1:
            return False
        elif position.x < 0 or position.y < 0:
            return False
        else:
            return True

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        borders = []
        if type(value) == tuple:
            value = board_position.BoardPosition(value[0], value[1])
        if type(value) == board_position.BoardPosition:
            value = value.to_rect()
        position = self.get_board_position_from_pixel(value.center)
        if position.x == self.columns - 1:
            borders.append("right")
        if position.y == self.rows - 1:
            borders.append("bottom")
        if position.x == 0:
            borders.append("right")
        if position.y == 0:
            borders.append("top")
        return borders
