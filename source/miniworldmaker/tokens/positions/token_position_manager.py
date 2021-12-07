import pygame

from typing import Union
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_position_factory
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
        self._position = 0
        self._direction = 0
        self._initial_direction = 0
        if position is not None:
            self._position = position
        else:
            self._position = (0, 0)

    @property
    def rect(self):
        return self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    @classmethod
    def from_center(cls, center_position: board_position.BoardPosition):
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
        self.set_direction(value)

    def get_direction(self):
        return (self._direction + 180) % 360 - 180

    def set_direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.token.costume_manager.rotate_costume()

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
            self.token.costume_manager.reload_costume()
        return self._size

    @property
    def position(self) -> board_position.BoardPosition:
        """
        The position of the token as tuple (x, y)
        """
        return self.get_position()

    @position.setter
    def position(self, value: tuple):
        self.set_position(value)

    def get_position(self) -> board_position.BoardPosition:
        return board_position_factory.BoardPositionFactory(self.token.board).create(self._position)

    def set_position(self, value):
        self.token.dirty = 1
        self.last_position = self.position
        self.last_direction = self.direction
        self._position = value
        if self.last_position != self._position:
            self.dirty = 1
            if self.token.board:
                self.token.board.app.event_manager.send_event_to_containers(
                    "token_moved", self.token)
        return self.position

    @property
    def center(self) -> board_position.BoardPosition:
        return self.get_center()

    @property
    def center_x(self):
        """x-value of token center-position"""
        if self.token.costume:
            return self.rect.centerx

    @center_x.setter
    def center_x(self, value):
        if self.costume is None:
            raise NoCostumeSetError(self.token)
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value
        self.x = rect.topleft[0]

    @property
    def center_y(self):
        """y-value of token center-position"""
        if self.token.costume:
            return self.rect.centery

    @center_y.setter
    def center_y(self, value):
        if self.costume is None:
            raise NoCostumeSetError(self.token)
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centery = value
        self.y = rect.topleft[1]

    @center.setter
    def center(self, value):
        self.set_center(value)

    def get_center(self):
        return board_position_factory.BoardPositionFactory(self.token.board).create((self.center_x, self.center_y))

    def set_center(self, value):
        if self.token.costume is None:
            raise NoCostumeSetError(self.token)
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value[0]
        rect.centery = value[1]
        self.position = rect.topleft

    @property
    def topleft(self) -> board_position.BoardPosition:
        return board_position_factory.BoardPositionFactory(self.token.board).create((self.rect.topleft[0], self.rect.topleft[1]))

    @topleft.setter
    def topleft(self, value):
        self.last_position = self.position
        self.position = value[0], value[1]

    def move(self, distance: int = 0):
        if distance == 0:
            distance = self.token.speed
        destination = self.token.board_sensor.get_destination(self.position, self.direction, distance)
        self.position = destination
        return self

    def move_in_direction(self, direction: Union[int, str], distance=1):
        direction = self._value_to_direction(direction)
        self.direction = direction
        self.move(distance)
        return self

    def move_back(self):
        self.position = self.last_position
        self.direction = self.last_direction
        return self

    def move_to(self, new_center_position: board_position.BoardPosition):
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
        if value == "left":
            value = 270
        if value == "right":
            value = 90
        if value == "down":
            value = 180
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
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
        return - (direction + 90) % 360 - 180

    def bounce_from_border(self, borders):
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        angle = self.direction
        if ("top" in borders and
                (self.direction <= 0 and self.direction > -90 or self.direction <= 90 and self.direction >= 0)):
            self.point_in_direction(0)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("bottom" in borders and (
                (self.direction < -90 and self.direction >= -180) or (self.direction > 90 and self.direction <= 180))):
            self.point_in_direction(180)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("left" in borders and self.direction <= 0):
            self.point_in_direction(-90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("right" in borders and (self.direction >= 0)):
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
        self.token.costume_manager.flip_costume(not self.token.costume.is_flipped)
        return self.direction

    def point_in_direction(self, direction: int) -> int:
        self.direction = self._value_to_direction(direction)
        return self.direction

    def remove(self):
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
