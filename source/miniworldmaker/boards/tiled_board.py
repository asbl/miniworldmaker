from collections import defaultdict
from typing import Union
import pygame
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.token import Token
from miniworldmaker.boards import board_position


class TiledBoard(Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=42, tile_margin=0):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            tile_size: The size of a tile
            tile_margin: The margin between tiles
        """
        super().__init__(columns=columns, rows=rows)
        self._tile_size = tile_size
        self._tile_margin = tile_margin
        self.set_size(self.tile_size, columns, rows, self._tile_margin)
        self._dynamic_actors_dict = defaultdict(list)  # the dict is regularly updated
        self._dynamic_actors = []  # List with all dynamic actors
        self._static_tokens_dict = defaultdict(list)

    def _update_token_positions(self) -> None:
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_colliding_tokens(self, token: Token) -> list:
        self._update_token_positions()
        colliding_tokens = self.get_tokens_in_area(token.rect)
        if token in colliding_tokens:
            colliding_tokens.remove(token)
        return colliding_tokens

    def get_tokens_in_area(self, area: Union[pygame.Rect, tuple], token_type=None, exclude=None) -> list:
        self._dynamic_actors_dict.clear()
        self._update_token_positions()
        if type(area) == tuple:
            position = board_position.BoardPosition(area[0], area[1])
        else:
            position = self.get_board_position_from_pixel(area.topleft)
        tokens_in_area = []
        if self.is_on_board(self.rect):
            if self._dynamic_actors_dict[position.x, position.y]:
                tokens_in_area.extend(self._dynamic_actors_dict[(position.x, position.y)])
            if self._static_tokens_dict[position.x, position.y]:
                tokens_in_area.extend(self._static_tokens_dict[(position.x, position.y)])
        if token_type is not None:
            tokens_in_area = self.filter_actor_list(tokens_in_area, token_type)
        return tokens_in_area

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
        if token.is_static:
            self._static_tokens_dict[position].append(token)
        else:
            self._dynamic_actors.append(token)
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

    def is_on_board(self, area: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> bool:
        if type(area) == tuple:
            area = board_position.BoardPosition(area[0], area[1])
        if type(area) == board_position.BoardPosition:
            area = area.to_rect()
        position = self.get_board_position_from_pixel(area.center)
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