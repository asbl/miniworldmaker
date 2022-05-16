import collections
import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError
import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_vector as board_vector
from typing import Union, Tuple
import numpy as np
import math


class Position(collections.namedtuple('Position', ['x', 'y'])):
    """
    A Position Object represents a position on a Board.

    As a subclass of namedtuple, Position is for
    performance reasons not mutable. 

    On a tiled board, the Position does not describe pixels
    but tiles coordinates.
    """

    def __str__(self):
        return str("Pos(" + str(round(self.x, 3)) + "," + str(round(self.y, 3)) + ")")

    @classmethod
    def from_vector(cls, vector: board_vector.Vector):
        """
        Transforms a miniworldmaker-Vector object to a position.
        :param vector: The vector
        :return: The Position
        """
        return cls(vector[0], vector[1])

    @classmethod
    def from_board_coordinates(cls, position):
        """
        Transforms board-coordinates to position

        :param position:
        :return: The Position
        """
        x = position[0]
        y = position[1]
        return cls(x, y)

    @classmethod
    def create(cls, value: Union[Tuple, "Position", "pygame.Rect"]):
        """Creates a board position from value

        If value is ...
        * Tuple: A new Position-object will be created
        * Position: The position object itself is returned
        * pygame.Rect: The position is created from topleft corner of Rect
        """
        if isinstance(value, tuple):
            return cls(value[0], value[1])
        elif type(value) == Position:
            return value
        elif type(value) == pygame.Rect:
            return cls(value.topleft)
        else:
            raise NoValidBoardPositionError(value)

    @classmethod
    def from_pixel(cls, position: Tuple):
        """
        Transforms pixel-coordinates to position by calling board.get_from_pixel()

        :param position:
        :return:
        """
        board = app.App.board
        position = board.get_from_pixel(position)
        return position[0], position[1]

    def to_pixel_from_tile(self):
        """
        Transforms position to pixel-coordinates by calling board.to_pixel()
        :return:
        """
        board = app.App.board
        return board.to_pixel(self)

    def add(self, x, y):
        """
        Adds x and y to the board positions x and y coordinate

        Returns:
            The new Position
        """
        return Position(self.x + x, self.y + y)

    def __add__(self, other: Union[Tuple, "Position", "board_vector.Vector"]):
        """
        Adds two board coordinates (or board-coordinate and vector)

        :param other: Position, Tuple or Vector with second position
        :return:
        """
        return Position(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Union[Tuple, "Position", "board_vector.Vector"]):
        if type(other) == Position:
            return Position(self.x - other.x, self.y - other.y)
        elif type(other) == tuple:
            return Position(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Position(-self.x, -self.y)

    def to_int(self):
        """
        Transforms both coordinates of a position to integers
        :return: Tuple (x,y) , x and y are integers.
        """
        return (int(self.x), int(self.y))

    def is_close(self, other : Union["Position", Tuple], error : int =1):
        """
        Is a position close to another position

        :param other: The other position
        :param error: The error for both coordinates.
        :return: If x-other.x < error and y-other.y < error, is_close() returns True
        """
        if abs(self.x - other[0]) < error and abs(self.y - other[1] < error):
            return True
        return False


class BoardPosition(Position):
    # legacy
    pass
