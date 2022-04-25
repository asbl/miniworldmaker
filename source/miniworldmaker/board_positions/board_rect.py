import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardRectError
import miniworldmaker.base.app as app


class Rect(pygame.Rect):

    @classmethod
    def create(cls, rect):
        if type(rect) == tuple:
            cls(rect[0], rect[1], 1, 1)
            return rect
        elif type(rect) == pygame.Rect:
            return cls(rect.x, rect.y, rect.width, rect.height)
        else:
            raise NoValidBoardRectError()

    @classmethod
    def from_position(cls, position, dimensions=None):
        board = app.App.board
        if dimensions is None:
            new_rect = pygame.Rect(0, 0, board.tile_size, board.tile_size)
        else:
            new_rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        new_rect.topleft = position
        return new_rect

    @classmethod
    def from_token(cls, token):
        return Rect.create(token.rect)

    @property
    def board(self):
        return app.App.board
