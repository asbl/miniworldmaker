from __future__ import annotations

import collections
from abc import ABC
from typing import TYPE_CHECKING
from typing import Union, Tuple

import miniworldmaker.base.app as app
import miniworldmaker.boards.board_templates.tiled_board.tile as tile_mod
import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError

if TYPE_CHECKING:
    import miniworldmaker.positions.vector as board_vector



class PositionBase(ABC):
    pass


class Position(collections.namedtuple("Position", ["x", "y"]), PositionBase):
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
    def from_vector(cls, vector: "board_vector.Vector"):
        """
        Transforms a miniworldmaker-Vector object to a position.
        :param vector: The vector
        :return: The Position
        """
        return cls(vector[0], vector[1])

    def distance_to(self, other):
        return app.App.running_board.distance_to(self, other)

    def direction_to(self, other):
        return app.App.running_board.direction_to(self, other)

    angle_to = direction_to

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
        elif type(value) == tile_mod.Tile:
            pos =  cls.create(value.position)
            return pos
        else:
            raise NoValidBoardPositionError(value)

    @classmethod
    def from_pixel(cls, position: Tuple):
        """
        Transforms pixel-coordinates to position by calling board.get_from_pixel()

        :param position:
        :return:
        """
        board = app.App.running_board
        position = board.get_from_pixel(position)
        return position[0], position[1]

    def to_pixel_from_tile(self):
        """
        Transforms position to pixel-coordinates by calling board.to_pixel()
        :return:
        """
        board = app.App.running_board
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
        return Position(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Position(-self.x, -self.y)

    def to_int(self):
        """
        Transforms both coordinates of a position to integers
        :return: Tuple (x,y) , x and y are integers.
        """
        return (int(self.x), int(self.y))

    def is_close(self, other: Union["Position", Tuple], error: int = 1):
        """
        Is a position close to another position

        :param other: The other position
        :param error: The error for both coordinates.
        :return: If x-other.x < error and y-other.y < error, is_close() returns True
        """
        if abs(self.x - other[0]) < error and abs(self.y - other[1] < error):
            return True
        return False

    def up(self, value):
        return self.__class__(self.x, self.y - value)

    def down(self, value):
        return self.__class__(self.x, self.y + value)

    def left(self, value):
        return self.__class__(self.x - value, self.y)

    def right(self, value):
        return self.__class__(self.x + value, self.y)

    def is_on_the_board(self):
        return app.App.running_board.position_is_in_container(self)


class BoardPosition(Position):
    # legacy
    pass
