import math
from typing import Union

import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_vector as board_vector
from miniworldmaker.exceptions.miniworldmaker_exception import MoveInDirectionTypeError
from miniworldmaker.exceptions.miniworldmaker_exception import NoCostumeSetError


class TokenPositionManager:
    def __init__(self, token, position):
        self.token = token
        self.last_position = (0, 0)
        self.last_direction = 90
        self._size = (0, 0)  # Tuple with size
        self._old_size = (0, 0)
        self._size = (1, 1)
        self.is_static = False
        self._position = (0, 0)
        self._direction = 0
        self._initial_direction = 0
        if position is not None:
            self._position = position
        else:
            self._position = (0, 0)

    def move_vector(self, vector):
        position = self.get_position()
        position = vector.add_to_position(position)
        self.set_position(position)

    @property
    def rect(self):
        return self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.token.position[0], self.token.position[1], self.size[0], self.size[1])

    @classmethod
    def from_center(cls, center_position: "board_position.Position"):
        """
        Creates a token with center at center_position

        Args:
            center_position: Center of token
        """
        obj = cls(position=(0, 0))  # temp positition
        obj.center = center_position  # pos set to center
        return obj

    @property
    def direction(self):
        return self.get_direction()

    @direction.setter
    def direction(self, value: int):
        self.token.dirty = 1
        self.set_direction(value)

    def get_direction(self):
        direction = (self._direction + 180) % 360 - 180
        return direction

    def set_direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.token.costume.rotated()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple):
        self.set_size(value)

    def set_size(self, value):
        if value != self._size:
            self._old_size = self._size
            self._size = value
            if self.token.costume:
                self.token.costume.reload_transformations_after("all")
        return self._size

    @property
    def position(self) -> "board_position.Position":
        """
        The position of the token as tuple (x, y)
        """
        return self.get_position()

    @position.setter
    def position(self, value: tuple):
        self.set_position(value)

    def get_position(self) -> "board_position.Position":
        return board_position.Position.create(self._position)

    def set_position(self, value):
        self.last_position = self.position
        self.last_direction = self.direction
        self._position = value
        if self.last_position != self._position:
            self.token.dirty = 1
            if self.token.board:
                self.token.board.app.event_manager.send_event_to_containers("token_moved", self.token)
        return self.position

    @property
    def center(self) -> "board_position.Position":
        return self.get_center()

    @property
    def center_x(self):
        """x-value of token center-position"""
        if self.token.costume:
            return self.rect.centerx

    @center_x.setter
    def center_x(self, value):
        self.set_center((value, self.center_y))

    @property
    def center_y(self):
        """y-value of token center-position"""
        if self.token.costume:
            return self.rect.centery

    @center_y.setter
    def center_y(self, value):
        if self.costume is None:
            raise NoCostumeSetError(self.token)
        self.set_center((self.center_x, value))

    @center.setter
    def center(self, value):
        self.set_center(value)

    def get_center(self):
        return board_position.Position.create((self.center_x, self.center_y))

    @property
    def local_center(self) -> "board_position.Position":
        return board_position.Position.create((self.center_x - self.topleft[0], self.center_y - self.topleft[1]))

    def set_center(self, value):
        if self.token.costume is None:
            raise NoCostumeSetError(self.token)
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value[0]
        rect.centery = value[1]
        self.set_position(rect.topleft)

    @property
    def topleft(self) -> "board_position.Position":
        return board_position.Position.create((self.rect.topleft[0], self.rect.topleft[1]))

    @topleft.setter
    def topleft(self, value):
        self.last_position = self.position
        self.set_position((value[0], value[1]))

    def move(self, distance: int = 0):
        if distance == 0:
            distance = self.token.speed
        destination = self.token.board_sensor.get_destination(self.position, self.direction, distance)
        self.position = destination
        return self

    def move_in_direction(self, direction: Union[int, str, "board_position.Position", tuple], distance=1):
        if type(direction) in [int, str]:
            direction = self._value_to_direction(direction)
            self.set_direction(direction)
        elif type(direction) in [board_position.Position, tuple]:
            self.point_towards_position(direction)
        else:
            raise MoveInDirectionTypeError(direction)
        self.move(distance)
        return self

    def move_back(self):
        self.position = self.last_position
        self.direction = self.last_direction
        return self

    def move_to(self, new_center_position: board_position.Position):
        self.center = new_center_position
        return self

    def _value_to_direction(self, value) -> int:
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
        elif value == "forward":
            value = self.direction
        elif value == "back":
            value = 360 - self.direction
        elif isinstance(value, board_vector.Vector):
            value = value.to_direction() % 360
        else:
            value = value % 360
        return value

    @staticmethod
    def dir_to_unit_circle(direction: float):
        """
        Transforms the current direction into standard-unit-circle direction

        Args:
            value: The direction in scratch-style
        """
        return -(direction + 90) % 360 - 180

    @staticmethod
    def unit_circle_to_dir(direction: float):
        """
        Transforms the current direction from standard-unit-circle direction
        into scratch-style coordinates

        Args:
            value: The direction in math unit circle style.
        """
        return -(direction + 90) % 360 - 180

    def bounce_from_border(self, borders):
        """Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        angle = self.direction
        if "top" in borders and (
                self.direction <= 0 and self.direction > -90 or self.direction <= 90 and self.direction >= 0
        ):
            self.point_in_direction(0)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif "bottom" in borders and (
                (self.direction < -90 and self.direction >= -180) or (self.direction > 90 and self.direction <= 180)
        ):
            self.point_in_direction(180)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif "left" in borders and self.direction <= 0:
            self.point_in_direction(-90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif "right" in borders and (self.direction >= 0):
            self.point_in_direction(90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        return self

    def bounce_from_token(self, other):
        """experimental: Bounces actor from another token
        Args:
            token: the token

        Returns: the actor

        """
        angle = self.token.direction
        self.token.move(-self.token.speed)
        self.token.point_towards_token(other)
        incidence = self.token.direction - angle
        self.token.turn_left(180 - incidence)
        return self.token

    def turn_left(self, degrees: int = 90) -> int:
        self.direction = self.direction - degrees
        return self.direction

    def turn_right(self, degrees: int = 90):
        self.direction = self.direction + degrees
        return self.direction

    def flip_x(self) -> int:
        """Flips actor

        Returns:
            int: new direction
        """
        self.turn_left(180)
        self.token.costume.flip(not self.token.costume.is_flipped)
        return self.direction

    def point_in_direction(self, direction: int) -> int:
        self.direction = self._value_to_direction(direction)
        return self.direction

    def self_remove(self):
        """
        Method is overwritten in subclasses
        """
        pass

    @property
    def x(self) -> float:
        return self.get_position()[0]

    @x.setter
    def x(self, value) -> float:
        self.set_position((value, self.y))

    @property
    def y(self) -> float:
        return self.get_position()[1]

    @y.setter
    def y(self, value: float):
        self.set_position((self.x, value))

    def draw_position(self):
        return (self.x, self.y)

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.center
        x = destination[0] - pos[0]
        y = destination[1] - pos[1]
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                self.token.direction = math.degrees(math.atan(m)) - 90
            else:
                # destination is right
                self.token.direction = math.degrees(math.atan(m)) + 90
            return self.token.direction
        else:
            m = 0
            if destination[1] > self.token.position[1]:
                self.token.direction = 180
                return self.token.direction
            else:
                self.token.direction = 0
                return self.token.direction
