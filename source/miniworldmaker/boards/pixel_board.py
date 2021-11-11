from typing import Union
from miniworldmaker.appearances import background

import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards import board  as board_module
import miniworldmaker.tokens.token as token_module
from miniworldmaker.boards.board_handler.board_token_handler import board_pixelboardtokenhandler as pixelboardhandler

class PixelBoard(board_module.Board):

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size : int = 1,
                 tile_margin : int = 0,
                 background_image=None
                 ):
            self.token_handler = pixelboardhandler.PixelBoardTokenHandler(self)
            super().__init__(columns, rows, tile_size, tile_margin, background_image)


    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        """
        Gets all borders a rect is touching

        Args:
            rect: The rect

        Returns: A list of borders, e.g. ["left", "top", if rect is touching the left an top border.

        """

    def get_tokens_at_rect(self, rect: pygame.Rect, singleitem=False, exclude=None, token_type=None) -> Union[token_module.Token, list]:
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
        filtered_tokens = self.tokens.copy()
        if exclude in filtered_tokens:
            filtered_tokens.remove(exclude)
        # Filter tokens by token_type
        if token_type is not None:
            if isinstance(token_type, token_module.Token):  # is_token_type a object?
                filtered_tokens = [token_type]
            else:
                if type(token_type) == str:  # is token_type a string
                    token_type = token_module.Token.find_subclass(token_type)
                if token_type:
                    for token in filtered_tokens:
                        filtered_tokens = [token for token in filtered_tokens if
                                           (issubclass(token.__class__, token_type) or token.__class__ == token_type)]
        # Get tokens at rect
        if not singleitem:
            return [token for token in filtered_tokens if token.rect.colliderect(rect)]
        else:
            for token in filtered_tokens:
                if token.rect.colliderect(rect):
                    return token
        # Collision handling
        if not singleitem:
            return [token for token in filtered_tokens if token.rect.colliderect(rect)]
        else:
            for a_token in filtered_tokens:
                if a_token.rect.colliderect(rect):
                    return a_token

    def is_on_board(self, position: board_position.BoardPosition) -> bool:
        self.position_handler.is_pos