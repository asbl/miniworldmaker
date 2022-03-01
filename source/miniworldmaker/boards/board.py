from typing import Union

import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards.token_connectors.pixel_board_connector import PixelBoardConnector
from miniworldmaker.tokens import token as token_module
from miniworldmaker.boards import base_board
import miniworldmaker


class Board(miniworldmaker.BaseBoard):
    """Board is a Board for pixel-perfect games. It is equivalent to PixelBoard
    """
    def __init__(
        self,
        columns: int = 400,
        rows: int = 400,
    ):
        self._tile_size = 1
        self._tile_margin = 0
        super().__init__(columns, rows)

    def get_token_connector(self, token):
        return PixelBoardConnector(self, token)


    def _filter_tokens_by_type(self, token_list, token_type):
        filtered_tokens = token_list
        # token class_name --> class
        if type(token_type) == str:  # is token_type a string
            token_type = self.find_token_class_for_name(token_type)
        # single token --> list
        if isinstance(token_type, token_module.Token):  # is_token_type a object?
            token_list = [token_type]
        # filter
        if token_type:
            filtered_tokens = [
                token
                for token in token_list
                if (issubclass(token.__class__, token_type) or token.__class__ == token_type)
            ]
        return filtered_tokens


