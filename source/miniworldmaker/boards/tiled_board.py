from collections import defaultdict
from typing import Union
import pygame
from miniworldmaker.board_positions import board_position, board_position_factory
from miniworldmaker.boards import board
from miniworldmaker.exceptions.miniworldmaker_exception import TiledBoardTooBigError
from miniworldmaker.boards.token_connectors import tiled_board_connector
import miniworldmaker


class TiledBoard(miniworldmaker.Board):
    def __init__(self, columns: int = 20, rows: int = 16):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            tile_size: The size of a tile
        """
        self.default_token_speed: int = 1
        if columns  > 1000 or rows > 1000:
            raise TiledBoardTooBigError(columns, rows, 40)
        super().__init__(columns=columns, rows=rows)
        self.tile_size = 40
        self.speed = 30
        self.dynamic_tokens_dict: defaultdict = defaultdict(list)  # the dict is regularly updated
        self.dynamic_tokens: set = set()  # Set with all dynamic actors
        self.static_tokens_dict: defaultdict = defaultdict(list)
        self.fixed_size = True
        self.rotatable_tokens = True

    def get_token_connector(self, token) -> "tiled_board_connector.TiledBoardConnector":
        return tiled_board_connector.TiledBoardConnector(self, token)

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

    def is_position_on_board(self, position: board_position.BoardPosition) -> bool:
        position = board_position_factory.BoardPositionFactory(self).create(position)
        return self.position_manager.is_position_on_board(position)

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        position = board_position_factory.BoardPositionFactory(self).create(value)
        return self.position_manager.get_borders_from_position(position)

    def _update_token_positions(self):
        """Updates the dynamic_tokens_dict.

        All positions of dynamic_tokens_dict are updated by reading the dynamic_tokens list.

        This method is called very often in self.sensing_tokens - The dynamic_tokens list should therefore be as small as possible.
        Other tokens should be defined as static.
        """
        self.dynamic_tokens_dict.clear()
        for token in self.dynamic_tokens:
            x, y = token.position[0], token.position[1]
            self.dynamic_tokens_dict[(x, y)].append(token)

    def sensing_tokens(self, position):
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        self._update_token_positions()  # This method can be a bottleneck!
        token_list = []
        if self.dynamic_tokens_dict[position[0], position[1]]:
            token_list.extend(self.dynamic_tokens_dict[(position[0], position[1])])
        if self.static_tokens_dict[position[1], position[1]]:
            token_list.extend(self.static_tokens_dict[(position[0], position[1])])
        token_list = [token for token in token_list]
        return token_list

    def sensing_token(self, position):
        token_list = self.sensing_tokens(position)
        if token_list is None or token_list == []:
            return None
        else:
            return token_list[0]

