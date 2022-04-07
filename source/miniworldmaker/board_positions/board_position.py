import collections
import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError
from miniworldmaker.app.app import App
import numpy as np
class Position(collections.namedtuple('Position', ['x', 'y'])):
    """
    A Position Object represents a position on a Board.

    As a subclass of namedtuple, Position is for
    performance reasons not mutable. 

    On a tiled board, the Position does not describe pixels
    but tiles coordinates.
    """

    def __str__(self):
        return str("Pos(" + str(round(self.x,3)) + "," + str(round(self.y,3)) + ")")

    @classmethod
    def from_matrix(cls, matrix):
        return Position(matrix.item(0,0), matrix.item(0,1))

    @classmethod
    def from_vector(cls, vector):
        return Position(vector[0], vector[1])

    @classmethod
    def create(cls, value):
        if isinstance(value, tuple):
            return cls(value[0], value[1])
        elif type(value) == Position:
            return value
        elif type(value) == pygame.Rect:
            return value.topleft
        else:
            raise NoValidBoardPositionError(value)

    @classmethod
    def from_pixel(cls, position: tuple):
        board = App.board
        position = board.get_from_pixel(position)
        return position[0], position[1]

    def to_pixel(self):
        board = App.board
        x,y = board.to_pixel()
        return x, y

    def up(self, value):
        """
        Gets the board position above the actual board-position

        Args:
            value: the number of fields above the actual position

        Returns:
            A new Position

        """
        return Position(self.x, self.y - value)

    def down(self, value):
        """
        Gets the board position below the actual board-position

        Args:
            value: the number of fields below the actual position

        Returns:
            A new Position

        """
        return Position(self.x, self.y + value)

    def left(self, value):
        """
        Gets the board position left of the the actual board-position

        Args:
            value: the number of fields left of the the actual position

        Returns:
            A new Position

        """
        return Position(self.x - value, self.y)

    def right(self, value):
        """
        Gets the board position right of the actual board-position

        Args:
            value: the number of fields right of the actual position

        Returns:
            A new Position

        """
        return Position(self.x + value, self.y - value)

    def add(self, x, y):
        """
        Adds x and y to the board positions x and y coordinate

        Returns: The new Position

        """
        return Position(self.x + x, self.y + y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def to_int(self):
        return (int(self.x), int(self.y))