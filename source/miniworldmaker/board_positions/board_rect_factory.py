import pygame
from miniworldmaker import app
from miniworldmaker.board_positions import board_position


class BoardRectFactory:

    def __init__(self, board):
        self.board = board

    def create(self, rect):
        if type(rect) == tuple:
            rect = pygame.Rect(rect[0], rect[1], 1, 1)
            return rect
        elif type(rect) == pygame.Rect:
            return rect
        else:
            raise Exception(f'No valid argument for create in board_rect_factory. Type is {type(rect)} ')


    def from_tiled_position(self, position):
        return self.from_rect_topleft(position)


    """
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
    """

    def from_rect_topleft(self, position = None, dimensions: pygame.Rect = None) -> pygame.Rect:
        if dimensions is None:
            new_rect = pygame.Rect(0, 0, self.board.tile_size, self.board.tile_size)
        else:
            new_rect = pygame.Rect.BoardRect(0, 0, dimensions.width, dimensions.height)
        # board position to pixel
        pixel_x = position.x * self.board.tile_size + position.x * self.board.tile_margin + self.board.tile_margin
        pixel_y = position.y * self.board.tile_size + position.y * self.board.tile_margin + self.board.tile_margin
        if position is not None:
            if dimensions is not None:
                new_rect.topleft = dimensions.topleft
            else:
                new_rect.topleft = (pixel_x, pixel_y)
        else:
            position = (0,0)
        return new_rect
