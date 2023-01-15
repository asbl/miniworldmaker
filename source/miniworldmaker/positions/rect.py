import pygame

import miniworldmaker.base.app as app
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardRectError
from typing import Union


class Rect(pygame.Rect):

    @classmethod
    def create(cls, rect: Union[tuple, pygame.Rect]):
        if type(rect) == tuple:
            cls(rect[0], rect[1], 1, 1)
            return rect
        elif type(rect) == pygame.Rect:
            return cls(rect.x, rect.y, rect.width, rect.height)
        else:
            raise NoValidBoardRectError("No valid board direction")

    @classmethod
    def from_position(cls, position, dimensions=None, board=None):
        if board is None:
            board = app.App.running_board
        if dimensions is None:
            new_rect = pygame.Rect(0, 0, board.tile_size, board.tile_size)
        else:
            new_rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        new_rect.topleft = position
        return new_rect

    @classmethod
    def from_token(cls, token):
        return Rect.create(token.get_global_rect())

    @property
    def board(self):
        return app.App.running_board
