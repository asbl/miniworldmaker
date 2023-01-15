from abc import ABC, abstractmethod
from typing import Union, Tuple

import miniworldmaker.positions.direction as board_direction
import miniworldmaker.positions.position as board_position
import miniworldmaker.positions.rect as board_rect
import miniworldmaker.positions.vector as board_vector
import pygame
from miniworldmaker.appearances import costume
from miniworldmaker.boards.board_templates.pixel_board import board
from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError
from miniworldmaker.exceptions.miniworldmaker_exception import NoCostumeSetError
from miniworldmaker.tokens import token as token_mod


class TokenPositionManager(ABC):
    def __init__(self, token: "token_mod.Token", board: "board.Board"):
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
        self.sticky = False  #
        self._position = board_position.Position.create((0, 0))

    def move_vector(self, vector: "board_vector.Vector") -> "token_mod.Token":
        position = self.get_position()
        position = vector.add_to_position(position)
        self.set_position(position)
        return self.token

    @property
    def rect(self):
        return self.get_local_rect()

    @abstractmethod
    def get_global_rect(self) -> "board_rect.Rect":
        """ Defines size of global rect (pixel coordinates)

        Rect-Position is set in subclasses
        """
        if self.token.costume:
            _rect = self.token.costume.get_rect()
        else:
            _rect = pygame.Rect(0, 0,
                                self.token.size[0], self.token.size[1])
        return _rect

    def get_global_world_rect(self):
        """Transforms global rect to window coordinates
        """
        _rect = self.get_global_rect()
        x = _rect[0] + self.token.board.topleft[0]
        y = _rect[1] + self.token.board.topleft[1]
        _rect.topleft = (x, y)
        return _rect

    @abstractmethod
    def get_local_rect(self) -> "board_rect.Rect":
        """Rect in local board coordinates (e.g. tiles in TiledBoard
        """
        pass

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
        self.set_direction(value)

    def get_direction(self):
        direction = (self._direction + 180) % 360 - 180
        return direction

    def set_direction(self, value: Union[int, float, str, "board_direction.Direction"]):
        if type(value) not in [int, float, str, board_direction.Direction, board_vector.Vector]:
            raise ValueError(f"Direction must be int, float, Direction or Vector but is {type(value)}")
        self.last_direction = self.direction
        direction = board_direction.Direction.create(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.token.costume.rotated()

    @property
    def size(self):
        return self.get_size()

    @size.setter
    def size(self, value: Union[int, float, tuple]):
        self.set_size(value)

    def get_size(self):
        return self._size

    def set_size(self, value: Union[int, float, tuple], scale=False):
        """Sets size of token

        Args:
            value (Union[int, float, tuple]):
                An int or float will be converted to tuple (e.g. 2 => (2,2) )
            scale: Should size set or should token be scaled.

        Raises:
            ValueError: Raises ValueError, if type not in [int, float, tuple]

        Returns:
            The token with changed values
        """
        if type(value) in [int, float]:
            if value < 0:
                raise ValueError("token.size must be >= 0")
            else:
                value = (value, value)
        if type(value) != tuple:
            raise ValueError("token size must be int, float or tuple")
        if not scale:
            if value != self._size:
                self._old_size = self._size
                self._size = value
                if self.token.costume:
                    self.token.costume.set_dirty("scale", costume.Costume.RELOAD_ACTUAL_IMAGE)
        else:
            if value != (1, 1):
                self._old_size = self._size
                self._size = self._size[0] * value[0], self._size[1] * value[1]
                if self.token.costume:
                    self.token.costume.set_dirty("scale", costume.Costume.RELOAD_ACTUAL_IMAGE)
        return self.token

    def scale_width(self, value):
        old_width = self.token.size[0]
        old_height = self.token.size[1]
        scale_factor = value / old_width
        self.set_size((value, old_height * scale_factor))

    def scale_height(self, value):
        old_width = self.token.size[0]
        old_height = self.token.size[1]
        scale_factor = value / old_height
        self.set_size((old_width * scale_factor, value))

    def set_width(self, value):
        if value < 0:
            raise ValueError("token width must be >= 0")
        self.set_size((value, self.token.size[1]))

    def set_height(self, value):
        if value < 0:
            raise ValueError("token height must be >= 0")
        self.set_size((self.token.size[0], value))

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

    def set_position(self, value: Union[tuple, "board_position.BoardPosition"]) -> "board_position.BoardPosition":
        self.last_position = self.position
        self.last_direction = self.direction
        self._position = board_position.Position.create(value)
        # self.token.board.camera.fetch_token(self.token)
        if self.last_position != self._position:
            self.token.dirty = 1
        return self.position

    @property
    def center(self) -> "board_position.Position":
        return self.get_center()

    @property
    def center_x(self):
        """x-value of token center-position"""
        if self.token.costume:
            return self.get_global_rect().centerx

    @center_x.setter
    def center_x(self, value):
        self.set_center((value, self.center_y))

    @property
    def center_y(self):
        """y-value of token center-position"""
        if self.token.costume:
            return self.get_global_rect().centery

    @center_y.setter
    def center_y(self, value):
        if self.token.costume is None:
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

    def set_center(self, value: Union[tuple, "board_position.Position"]) -> "token_mod.Token":
        if self.token.costume is None:
            raise NoCostumeSetError(self.token)
        new_center = board_position.Position.create(value)
        self.last_position = self.position
        rect = pygame.Rect.copy(self.get_global_rect())
        rect.center = new_center
        self.set_position(rect.topleft)
        return self.token

    @property
    def topleft(self) -> "board_position.Position":
        return board_position.Position.create(self.get_global_rect().topleft)

    @topleft.setter
    def topleft(self, value):
        self.last_position = self.position
        self.set_position(value)

    def move(self, distance: int = 0):
        if distance == 0:
            distance = self.token.speed
        destination = self.token.board_sensor.get_destination(self.position, self.direction, distance)
        self.position = destination
        return self

    def move_towards_position(self, position, distance=1):
        tkn_center = board_position.Position.create(self.token.center)
        if tkn_center.is_close(position):
            return self
        else:
            direction = board_direction.Direction.from_token_to_position(self.token, position).value
            self.set_direction(direction)
            self.move(distance)
            return self

    def move_in_direction(self, direction: Union[int, str, "board_direction.Direction"], distance=1):
        if type(direction) in [int, str]:
            direction = board_direction.Direction.from_token_towards_direction(self.token, direction).value
            self.set_direction(direction)
            self.move(distance)
            return self
        elif type(direction) in [tuple, board_position.Position]:
            return self.move_towards_position(direction)
        else:
            raise MiniworldMakerError(
                f"No valid type in method move_in_direction - Expected int, str, Position or tuple, got {type(direction)}"
            )

    def undo_move(self):
        self.position = self.last_position
        self.direction = self.last_direction
        return self

    def move_to(self, new_center_position: Union[Tuple, "board_position.Position"]):
        self.center = new_center_position
        return self

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

    def turn_left(self, degrees: float = 90) -> int:
        self.direction = self.direction - degrees
        return self.direction

    def turn_right(self, degrees: float = 90):
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

    def point_in_direction(
            self, direction: Union[int, float, "board_direction.Direction", str]
    ) -> "board_direction.Direction":
        self.direction = board_direction.Direction.create(direction)
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

    def point_towards_position(
            self, destination: Union[int, float, str, "board_direction.Direction"]
    ) -> "board_direction.Direction":
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        direction = board_direction.Direction.create((self.token.center, destination))
        self.set_direction(direction.value)
        return self.direction

    def remove_from_board(self):
        pass
