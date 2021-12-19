from typing import Union

import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards import board as board_module
from miniworldmaker.boards.token_connectors.pixel_board_connector import PixelBoardConnector
from miniworldmaker.tokens import token as token_module
import miniworldmaker

class PixelBoard(miniworldmaker.Board):

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size: int = 1,
                 tile_margin: int = 0,
                 background_image=None
                 ):
        super().__init__(columns, rows, tile_size, tile_margin, background_image)

    def get_token_connector(self, token):
        return PixelBoardConnector(self, token)

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        """
        Gets all borders a rect is touching

        Args:
            rect: The rect

        Returns: A list of borders, e.g. ["left", "top", if rect is touching the left an top border.

        """
        pass

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
            filtered_tokens = [token for token in token_list if
                               (issubclass(token.__class__, token_type) or token.__class__ == token_type)]
        return filtered_tokens

    def get_tokens_at_rect(self, rect: pygame.Rect) -> list:
        """Returns all tokens that collide with a rectangle.

        Args:
            rect: A rectangle
            token_type: The class of the tokens which should be added
            singleitem: Should the return type be a single token (faster) or a list of tokens(slower)
            exclude: A token which should not be returned e.g. the actor itself

        Returns:
            If singleitem = True, the method returns all tokens colliding with the rect of the given token_type as list.
            If singleitem = False, the method returns the first token.

        """
        return [token for token in self.tokens if token.rect.colliderect(rect)]
    

    def get_single_token_at_rect(self, rect: pygame.Rect) -> token_module.Token:
        # Get first colliding token
        for token in self.tokens:
            if token.rect.colliderect(rect):
                return token
        return []

    def is_on_board(self, position: board_position.BoardPosition) -> bool:
        self.position_handler.is_pos
