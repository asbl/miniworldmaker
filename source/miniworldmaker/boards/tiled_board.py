from collections import defaultdict
from typing import Union
import pygame
from miniworldmaker.board_positions import board_position, board_position_factory
from miniworldmaker.boards import board
from miniworldmaker.exceptions.miniworldmaker_exception import TiledBoardTooBigError
from miniworldmaker.boards.token_connectors import tiled_board_connector
import miniworldmaker


class TiledBoard(miniworldmaker.Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=42, tile_margin=0, background_image=None):
        """Initializes the TiledBoard

        Args:
            columns: The number of columns
            rows: The number of rows
            tile_size: The size of a tile
            tile_margin: The margin between tiles
        """
        self.default_token_speed: int = 1
        self.dynamic_tokens_dict: defaultdict = defaultdict(list)  # the dict is regularly updated
        self.dynamic_tokens: list = []  # List with all dynamic actors
        self.static_tokens_dict: defaultdict = defaultdict(list)
        if columns * tile_size > 8000 or rows * tile_size > 8000:
            raise TiledBoardTooBigError(columns, rows, tile_size)
        super().__init__(columns=columns, rows=rows, tile_size=tile_size, tile_margin=tile_margin,
                         background_image=background_image)

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

    def is_position_on_board(self, value: tuple) -> bool:
        """
        Checks if position is on board

        Args:
            value: A Board Position or a board rect

        Returns:

        """
        position = board_position_factory.BoardPositionFactory(self).create(value)
        return self.position_handler.is_position_on_board(position)

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        """

        Args:
            value:

        Returns:

        """
        position = board_position_factory.BoardPositionFactory(self).create(value)
        return self.position_handler.get_borders_from_position(position)

    def _update_token_positions(self):
        self.dynamic_tokens_dict.clear()
        for token in self.dynamic_tokens:
            x, y = token.position[0], token.position[1]
            self.dynamic_tokens_dict[(x, y)].append(token)

    def sensing_tokens(self, position):
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        self._update_token_positions()
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
