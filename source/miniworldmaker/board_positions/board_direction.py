import math
from typing import Union, Tuple

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_vector as board_vector
from miniworldmaker.exceptions.miniworldmaker_exception import MoveInDirectionTypeError
from miniworldmaker.tokens import token as token_mod

class Direction(int):
    def __init__(self, direction):
        self.value = direction

    @classmethod
    def create(cls, direction: Union[int, str, Tuple, "board_vector.Vector", "Direction"]):
        """
        Create Board-Direction from. int, str or two points.
        :param direction: int: Integer value direction, str: Str Direction ("e.g." "right"), or Tuple[Position, Position]
            with two points.
        :return:
        """
        if type(direction) in [int, float, str, board_vector.Vector]:
            direction = cls._value_to_direction(direction)
            _dir_obj = cls(direction)
        elif type(direction) in [tuple]:
            # tuple with two points
            _dir_obj = cls.from_two_points(direction[0], direction[1])
        elif type(direction) == Direction:
            return direction
        else:
            raise MoveInDirectionTypeError(direction)
        return _dir_obj

    @classmethod
    def create_from_token(cls, token : "token_mod.Token", direction : Union[int, float, "Direction"]) -> "Direction":
        if type(direction) in [int, str]:
            direction = cls._value_from_token_to_direction(token, direction)
            _dir_obj = cls(direction)
        elif type(direction) == tuple:
            _dir_obj = cls.from_two_points(token.position, (direction[0], direction[1]))
        else:
            raise MoveInDirectionTypeError(direction)
        return _dir_obj

    @classmethod
    def from_two_points(cls, pos1: Union[tuple, "board_position.BoardPosition"], pos2 : Union[tuple, "board_position.BoardPosition"]) -> "Direction":
        x = pos2[0] - pos1[0]
        y = pos2[1] - pos1[1]
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                direction = math.degrees(math.atan(m)) - 90
            else:
                # destination is right
                direction = math.degrees(math.atan(m)) + 90
            return cls(direction)
        else:
            m = 0
            if pos2[1] > pos1[1]:
                direction = 180
            else:
                direction = 0
            return cls(direction)

    @staticmethod
    def _value_to_direction(value) -> int:
        """
        Transforms a string value ("top", "left", "right", "bottom)
        into a position

        Args:
            value: The String value ("top", "left", "right", or "bottom)

        Returns:
            The position as scratch-style deegrees

        """
        if value == "top" or value == "up":
            value = 0
        elif value == "left":
            value = 270
        elif value == "right":
            value = 90
        elif value == "down":
            value = 180
        elif isinstance(value, board_vector.Vector):
            value = value.to_direction() % 360
        else:
            value = value % 360
        return value

    @staticmethod
    def _value_from_token_to_direction(token: "token_mod.Token", value) -> int:
        if value == "forward":
            return token.direction
        elif value == "back":
            return 360 - token.direction
        else:
            return Direction._value_to_direction(value)
