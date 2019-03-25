from collections import defaultdict
from typing import Union
import pygame
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.token import Token


class TiledBoard(Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=16, tile_margin=0):
        super().__init__(columns=columns, rows=rows)
        self._tile_size = tile_size
        self._tile_margin = tile_margin
        self.set_size(self.tile_size, columns, rows, self._tile_margin)
        self._dynamic_actors_dict = defaultdict(list)  # the dict is regularly updated
        self._dynamic_actors = []  # List with all dynamic actors
        self._static_tokens_dict = defaultdict(list)

    def show_grid(self):
        """
        Draws the grid on the background
        """
        self.set_image_action("grid_overlay", True)

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

    def get_tokens_in_area(self, value: Union[pygame.Rect, tuple], token_type=None) -> list:
        self._dynamic_actors_dict.clear()
        self._update_token_positions()
        if type(value) == tuple:
            x, y = value[0], value[1]
        else:
            x, y = self.to_board_position(value.topleft)
        tokens_in_area = []
        if self.on_board(self.rect):
            if self._dynamic_actors_dict[x, y]:
                tokens_in_area.extend(self._dynamic_actors_dict[(x, y)])
            if self._static_tokens_dict[x, y]:
                tokens_in_area.extend(self._static_tokens_dict[(x, y)])
        if token_type is not None:
            tokens_in_area = self.filter_actor_list(tokens_in_area, token_type)
        return tokens_in_area

    def remove_from_board(self, token: Token) -> None:
        print("remove", token)
        if token in self._dynamic_actors:
            self._dynamic_actors.remove(token)
        if token in self._static_tokens_dict[(token.x, token.y)]:
            self._static_tokens_dict[(token.x, token.y)].remove(token)
        super().remove_from_board(token)

    def remove_tokens_in_area(self, value: Union[pygame.Rect, tuple], actor_type=None) -> None:
        """
        Removes all actors in an area
        Args:
            value: Either rectangle or grid-position
            actor_type: The actor type which should be removed

        Returns: true if any actor was removed
        """
        actors = self.get_tokens_in_area(value, actor_type)
        for actor in actors:
            self.remove_from_board(actor)

    def add_to_board(self, token: Token, position: tuple = None) -> Token:
        if token.is_static:
            self._static_tokens_dict[(position[0], position[1])].append(token)
        else:
            self._dynamic_actors.append(token)
        super().add_to_board(token, position)
        if token.size == (0, 0):
            token.size = (self.tile_size, self.tile_size)
        token.changed()
        return token

    def update_token(self, token: Token, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_tokens_dict[(token.x(), token.y())].append(token)
            if token in self._dynamic_actors_dict:
                self._dynamic_actors_dict.pop(token)
        else:
            self._dynamic_actors.append(token)

    def is_empty_cell(self, position: tuple) -> bool:
        """
        Checks if cell is empty
        :param position: the position of the cell
        :return: True if cell is empty
        """
        if not self.get_tokens_in_area(position):
            return True
        else:
            return False

    @staticmethod
    def get_neighbour_cells(position: tuple) -> list:
        """
        Gets a list with all neighbour cells
        :param position: The position of the cell
        :return: the neighbour cells as list
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

    def on_board(self, value: Union[tuple, pygame.Rect]) -> bool:
        if type(value) == tuple:
            value = self.tile_to_rect(value)
        x, y = self.to_board_position(value.center)
        if x > self.columns - 1:
            return False
        elif y > self.rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def borders(self, value: Union[tuple, pygame.Rect]) -> list:
        borders = []
        if type(value) == tuple:
            value = self.tile_to_rect(value)
        x, y = self.to_board_position(value.center)
        if x == self.columns - 1:
            borders.append("right")
        if y == self.rows - 1:
            borders.append("bottom")
        if x == 0:
            borders.append("right")
        if y == 0:
            borders.append("top")
        return borders