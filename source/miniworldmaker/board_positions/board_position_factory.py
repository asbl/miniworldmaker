from miniworldmaker.board_positions import board_position
import pygame

from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError

class BoardPositionFactory:

    def __init__(self, board):
        self.board = board

    def from_pixel(self, position: tuple):
        board = self.board
        column = (position[0] - board.tile_margin) // (board.tile_size + board.tile_margin)
        row = (position[1] - board.tile_margin) // (board.tile_size + board.tile_margin)
        return column, row

    def from_float(self, float_position: tuple):
        x = int(float_position[0])
        y = int(float_position[1])
        return board_position.BoardPosition(x,y)

    def from_tuple(self, tpl: tuple):
        """
        Gets a board position from tuple.

        Args:
            tpl: The tuple

        Returns:

        """
        return board_position.BoardPosition(tpl[0], tpl[1])

    def from_rect_center(self, rect):
        """
        Gets a board position from rect.
        The BoardPosition is the center-position of the rectangle

        Args:
            rect: The rectangle

        Returns:

        """
        BoardPositionFactory.create(rect)
        return self.from_pixel(rect.center)

    def create(self, value):
        if isinstance(value, tuple):
            return board_position.BoardPosition(value[0], value[1])
        elif type(value) == board_position.BoardPosition:
            return value
        elif type(value) == pygame.Rect:
            return value.topleft
        else:
            raise NoValidBoardPositionError(value)

    def to_pixel(self) -> tuple:
        """
        Converts board_position to pixel-coordinates.
          * If the board is a PixelBoard, these are the same values.
          * If the board is a TiledBoard, the top-left corner of a tile is returned.

        Returns: The Top-Left Pixel of current board-position

        """
        rect = self.to_rect()
        return rect.topleft