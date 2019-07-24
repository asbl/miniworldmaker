from collections import defaultdict
from typing import Union

import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens import tiled_connector


class TiledBoard(Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=42, tile_margin=0):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            tile_size: The size of a tile
            tile_margin: The margin between tiles
        """
        self.default_token_speed = 1
        self.dynamic_tokens_dict = defaultdict(list)  # the dict is regularly updated
        self.dynamic_tokens = []  # List with all dynamic actors
        self.static_tokens_dict = defaultdict(list)
        super().__init__(columns=columns, rows=rows, tile_size=tile_size, tile_margin=tile_margin)
        self.speed = 30


    def add_to_board(self, token, position):
        """
        Adds token to board.
        This method is called with token.__init__
        Args:
            token:
            position:

        Returns:

        """
        super().add_to_board(token, position)
        token.board_connector = tiled_connector.TiledBoardConnector(token, self)

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

    def on_board(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> bool:
        pos = self._get_position_from_parameter(value)
        return pos.is_on_board()

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        """

        Args:
            value:

        Returns:

        """
        pos = self._get_position_from_parameter(value)
        return pos.borders()

    def _get_position_from_parameter(self, parameter):
        if type(parameter) == tuple:
            pos = board_position.BoardPosition(parameter[0], parameter[1])
        elif type(parameter) == board_position.BoardPosition:
            pos = parameter
        elif type(parameter) == pygame.Rect:
            pos = board_position.BoardPosition.from_rect(value)
        else:
            raise TypeError("Parameter must be tuple, BoardPosition or Rect")
        return parameter