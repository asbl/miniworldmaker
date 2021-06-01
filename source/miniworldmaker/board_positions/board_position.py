import collections

import pygame
from miniworldmaker.app import app
from miniworldmaker.board_positions import board_rect


class BoardPosition(collections.namedtuple('Point', ['x', 'y'])):
    """
    A BoardPosition Object represents a position on a Board.

    As a subclass of namedtuple, BoardPosition is for
    performance reasons not mutable.

    On a tiled board, the BoardPosition does not describe pixels
    but tiles coordinates.
    """
    def __str__(self):
        return str("Pos(" + str(self.x) + "," + str(self.y) + ")")

    def __eq__(self, other):
        board = app.App.board
        return self.near(other, board.default_token_speed - 1)

    @classmethod
    def from_pixel(cls, position: tuple):
        """
        Gets the board_position from pixel coordinates

        If the board is a pixel-board, pixel-position and board_position are the same

        Args:
            position: The board position as pixel-coordinates

        Returns:

        """
        board = app.App.board
        column = (position[0] - board.tile_margin) // (board.tile_size + board.tile_margin)
        row = (position[1] - board.tile_margin) // (board.tile_size + board.tile_margin)
        return cls(column, row)

    @classmethod
    def from_float(cls, float_position : tuple):
        """
        Gets a board_position from float and convert the float values into integer.
        If you don't want the position converted into a integer-value, use from_tuple

        Args:
            float_position: Float position

        Returns:

        """
        x = int(float_position[0])
        y = int(float_position[1])
        return cls(x,y)

    @classmethod
    def from_tuple(cls,tpl : tuple):
        """
        Gets a board position from tuple.

        Args:
            tpl: The tuple

        Returns:

        """
        return cls(tpl[0],tpl[1])

    @classmethod
    def from_rect(cls, rect: board_rect.BoardRect):
        """
        Gets a board position from rect.
        The BoardPosition is the center-position of the rectangle

        Args:
            rect: The rectangle

        Returns:

        """
        return BoardPosition.from_pixel(rect.center)

    def near(self, other, distance):
        """
        Checks if two Board-Positions are near each other

        Args:
            other: A second Board-Position.
            distance: The size of the environment in which 2 positions are called "near".

        Returns:
            True, If the Positions are near each other.

        """
        if isinstance(other, tuple):
            other = BoardPosition(other[0], other[1])
        if isinstance(other, BoardPosition):
            if self.x <= other.x + distance \
                    and self.x >= other.x - distance \
                    and self.y <= other.y + distance \
                    and self.y >= other.y - distance:
                return True
        else:
            return False

    def to_pixel(self) -> tuple:
        """
        Converts board_position to pixel-coordinates.
          * If the board is a PixelBoard, these are the same values.
          * If the board is a TiledBoard, the top-left corner of a tile is returned.

        Returns: The Top-Left Pixel of current board-position

        """
        rect = self.to_rect()
        return rect.topleft

    def to_rect(self, rect: pygame.Rect = None) -> board_rect.BoardRect:
        """
        Converts a board position into a rect.
        The board_position is at the top-left corner of the rect.

        Args:
            rect: The rect dimensions (x and y coordinates are ignored. If rect is None,
            the board.tile_size is used instead.

        Returns: The rect at the given position

        """
        board = app.App.board
        if rect is None:
            new_rect = board_rect.BoardRect(0, 0, board.tile_size, board.tile_size)
        else:
            new_rect = board_rect.BoardRect(0, 0, rect.width, rect.height)
        # board position to pixel
        pixel_x = self.x * board.tile_size + self.x * board.tile_margin + board.tile_margin
        pixel_y = self.y * board.tile_size + self.y * board.tile_margin + board.tile_margin
        new_rect.topleft = (pixel_x, pixel_y)
        return new_rect

    def to_tuple(self):
        """
        Converts board_position into a tuple (x, y)

        Returns: The boar

        """
        return self.x, self.y

    def up(self, value: int):
        """
        Gets the board position above the actual board-position

        Args:
            value: the number of fields above the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y - value)

    def down(self, value: int):
        """
        Gets the board position below the actual board-position

        Args:
            value: the number of fields below the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y + value)

    def left(self, value: int):
        """
        Gets the board position left of the the actual board-position

        Args:
            value: the number of fields left of the the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x - value, self.y)

    def right(self, value: int):
        """
        Gets the board position right of the actual board-position

        Args:
            value: the number of fields right of the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x + value, self.y - value)

    def add(self, x, y):
        """
        Adds x and y to the board positions x and y coordinate

        Returns: The new BoardPosition

        """
        return BoardPosition(self.x + x, self.y + y)

    def is_on_board(self):
        """
        Checks if BoardPosition is on board

        Returns:
            True, if Position is on board.
        """
        board = app.App.board
        if self.x >= 0 and self.y >= 0 and self.x < board.columns and self.y < board.rows:
            return True
        else:
            return False

    def borders(self):
        """
        Gets borders of a board-position

        Returns:

        """
        rect = self.to_rect()
        board =  app.App.board
        position = board.get_board_position_from_pixel(rect.center)
        borders = []
        if position.x == board.columns - 1:
            borders.append("right")
        if position.y == board.rows - 1:
            borders.append("bottom")
        if position.x == 0:
            borders.append("right")
        if position.y == 0:
            borders.append("top")
        return borders

    def color(self):
        """
        Returns the board-color at the current board-position

        Returns: The board-color at the current board position as tuple
        with r,g,b value and transparency (e.g. (255, 0, 0, 100)

        """
        board = app.App.board
        if self.is_on_board():
            return board.background.color_at(self.to_pixel())
        else:
            return ()
