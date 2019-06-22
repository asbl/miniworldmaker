import collections

import pygame
from miniworldmaker.windows import miniworldwindow as window


class BoardPosition(collections.namedtuple('Point', ['x', 'y'])):
    """
    A BoardPosition Object represents a position on a Board.

    As a subclass of namedtuple, BoardPosition is for
    performance reasons not mutable.

    On a tiled board, the BoardPosition does not describe pixels
    but tiles coordinates.
    """

    def __eq__(self, other):
        board = window.MiniWorldWindow.board
        return self.near(other, board.default_actor_speed-1)

    @classmethod
    def from_pixel(cls, position: tuple):
        board = window.MiniWorldWindow.board
        column = (position[0] - board.tile_margin) // (board.tile_size + board.tile_margin)
        row = (position[1] - board.tile_margin) // (board.tile_size + board.tile_margin)
        return cls(column, row)

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
            other = BoardPosition(other[0],other[1])
        if isinstance(other, BoardPosition):
            if self.x <= other.x + distance \
                    and self.x >= other.x - distance \
                    and self.y <= other.y + distance \
                    and self.y >= other.y - distance:
                return True
        else:
            return False

    def to_tuple(self):
        return self.x, self.y

    def to_rect(self, rect: pygame.Rect = None) -> pygame.Rect:
        board = window.MiniWorldWindow.board
        if rect is None:
            new_rect = pygame.Rect(0, 0, board.tile_size, board.tile_size)
        else:
            new_rect = pygame.Rect(0, 0, rect.width, rect.height)
        # board position to pixel
        pixel_x = self.x * board.tile_size + self.x * board.tile_margin + board.tile_margin
        pixel_y = self.y * board.tile_size + self.y * board.tile_margin + board.tile_margin
        new_rect.topleft = (pixel_x, pixel_y)
        return new_rect

    def __str__(self):
        return str("Pos(" + str(self.x) + "," + str(self.y) + ")")

    def up(self, value: int):
        """
        Gets the board position above the actual board-position

        Args:
            value: the number of fields above the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y-value)

    def down(self, value: int):
        """
        Gets the board position below the actual board-position

        Args:
            value: the number of fields below the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x, self.y+value)

    def left(self, value: int):
        """
        Gets the board position left of the the actual board-position

        Args:
            value: the number of fields left of the the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x-value, self.y)

    def right(self, value: int):
        """
        Gets the board position right of the actual board-position

        Args:
            value: the number of fields right of the actual position

        Returns:
            A new BoardPosition

        """
        return BoardPosition(self.x+value, self.y-value)

    def add(self, x, y):
        return BoardPosition(self.x+x, self.y+y)

    def to_pixel(self) -> tuple:
        rect = self.to_rect()
        return rect.topleft

    def is_on_board(self):
        """
        Checks if BoardPosition is on board

        Returns:
            True, if Position is on board.
        """
        board = window.MiniWorldWindow.board
        if self.x >= 0 and self.y >= 0 and self.x < board.columns and self.y < board.rows:
            return True
        else:
            return False
