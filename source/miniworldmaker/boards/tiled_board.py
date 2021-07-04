from collections import defaultdict
from typing import Union

from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect
from miniworldmaker.boards import board
from miniworldmaker.connectors import tiled_connector
from miniworldmaker.board_positions import board_rect

class TiledBoard(board.Board):

    def __init__(self, columns: int = 20, rows: int = 16, tile_size=42, tile_margin=0, background_image=None):
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
        super().__init__(columns=columns, rows=rows, tile_size=tile_size, tile_margin=tile_margin,
                         background_image=background_image)

    def _add_board_connector(self, token, position):
        token.position = position
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

    def on_board(self, value: Union[tuple, board_position.BoardPosition, board_rect.BoardRect]) -> bool:
        """
        Checks if position is on board

        Args:
            value: A Board Position or a board rect

        Returns:

        """
        pos = self._get_position_from_parameter(value)
        return pos.is_on_board()

    def borders(self, value: Union[tuple, board_position.BoardPosition, board_rect.BoardRect]) -> list:
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
        elif type(parameter) == board_rect.BoardRect:
            pos = board_position.BoardPosition.from_rect(parameter)
        else:
            raise TypeError("Parameter must be tuple, BoardPosition or Rect")
        return parameter

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
        