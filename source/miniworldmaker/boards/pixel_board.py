from typing import Union

import pygame
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect
from miniworldmaker.boards import board as bd
from miniworldmaker.connectors import pixel_connector
from miniworldmaker.tokens import token as tk


class PixelBoard(bd.Board):

    def _add_board_connector(self, token, position):
        token.board_connector = pixel_connector.PixelBoardConnector(token, self)
        token.topleft = position[0], position[1]

    def remove_from_board(self, token: tk.Token):
        """
        removes a token from board.
        The method is called with token.remove()

        Args:
            token: The token to remove from board.

        Returns:

        """
        super().remove_from_board(token)

    def borders(self, value: Union[tuple, board_position.BoardPosition, pygame.Rect]) -> list:
        """
        Gets all borders a rect is touching

        Args:
            rect: The rect

        Returns: A list of borders, e.g. ["left", "top", if rect is touching the left an top border.

        """

    def get_tokens_at_rect(self, rect: pygame.Rect, singleitem=False, exclude=None, token_type=None) -> Union[
        tk.Token, list]:
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
            if isinstance(token_type, tk.Token):  # is_token_type a object?
                filtered_tokens = [token_type]
            else:
                if type(token_type) == str:  # is token_type a string
                    token_type = tk.Token.find_subclass(token_type)
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

    def _get_rect_from_parameter(self, parameter):
        if type(parameter) == tuple:
            rect = board_position.BoardPosition(parameter[0], parameter[1]).to_rect()
        elif type(parameter) == board_position.BoardPosition:
            rect = parameter.to_rect()
        elif type(parameter) == board_rect.BoardRect:
            rect = parameter
        else:
            raise TypeError("Parameter must be tuple, BoardPosition or Rect")
        return parameter
