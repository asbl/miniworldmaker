import math
from logging import *
from typing import Union

import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.physics import physics as ph
from miniworldmaker.tokens import costume
from miniworldmaker.windows import miniworldwindow


class Token(pygame.sprite.DirtySprite):

    token_count = 0
    log = getLogger("Token")
    lookup = True
    class_image = None

    def __init__(self, position = None):
        self.board = None
        super().__init__()
        self.costume = None
        # private
        self._size = (0, 0)  # Tuple with size
        self._position: board_position = position
        self._on_board = False
        self._is_at_border = False
        self._at_borders_list = False
        self._is_flipped = False
        Token.token_count += 1
        self._direction = 0
        # public
        self.physics = None
        self.last_position = (0,0)
        self.last_direction = 90
        self.token_id = Token.token_count + 1
        self.is_static = True
        self.registered_event_handlers = dict()
        # costume
        self.costume = costume.Costume(self)
        self._image = pygame.Surface((1, 1))
        self._rect = self._image.get_rect()
        self.costumes = [self.costume]
        self.costume.is_upscaled = True
        self.costume.orientation = 0
        self.init = 1
        self.speed = 0
        self.setup_physics()
        if position is not None:
            self.board = miniworldwindow.MiniWorldWindow.board
            self.board.add_to_board(self, position)
        else:
            board = None
        self._dirty = 1


    @property
    def is_flipped(self):
        return self.costume.is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self.costume._is_flipped = value
        if self.is_flipped is True:
            self.costume.enabled_image_actions["flip"] = True
            self.costume.call_action("flip")
        else:
            self.costume.enabled_image_actions["flip"] = False
            self.costume.call_action("flip")

    def __str__(self):
        if self.board:
            return "{0}-Object, ID: {1} at pos {2}".format(self.class_name, self.token_id, self.position)
        else:
            return "**: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._image = self.costume.image
            return self.costume.image

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if hasattr(self, "board") and self.board:
            self.board.dirty = 1

    @property
    def rect(self):
        if self.dirty == 1:
            self._rect = self.position.to_rect(rect=self.image.get_rect())
            return self._rect
        else:
            return self._rect

    def add_image(self, path: str) -> int:
        image = self.costume.add_image(path)
        if not self.__class__.class_image:
            self.__class__.class_image = path
        return image

    def add_costume(self, path: str) -> costume.Costume:
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        new_costume.orientation = self.costume.orientation
        self.costumes.append(new_costume)
        return new_costume

    def switch_costume(self, index=-1) -> costume.Costume:
        """Switches costume

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: The new costume

        """
        if index == -1:
            index = self.costumes.index(self.costume)
            if index < len(self.costumes) - 1:
                index += 1
            else:
                index = 0
        else:
            index = index
        self.costume = self.costumes[index]
        self.costume.dirty = 1
        self.costume.changed_all()
        self.dirty = 1
        return self.costume

    def add_to_board(self, board, position: board_position.BoardPosition):
        try:
            self.board = board
            self.position = position
            self.costume.changed_all()
            self.dirty = 1
            if self.init != 1:
                raise UnboundLocalError("Init was not called")
            self.board.window.send_event_to_containers("actor_created", self)
        except UnboundLocalError:
            raise

    @property
    def direction(self) -> int:
        """ Sets direction the token is oriented

            0°:  East, x degrees clock-wise otherwise
            You can also set the direction by String ("forward", "up", "down", ...
        """
        return (self._direction + 180) % 360 - 180

    @property
    def direction_at_unit_circle(self):
        return  Token.dir_to_unit_circle(self._direction)

    @direction_at_unit_circle.setter
    def direction_at_unit_circle(self, value):
        self.direction = Token.unit_circle_to_dir(value)

    @staticmethod
    def dir_to_unit_circle(direction):
        return -(direction + 90) % 360 - 180

    @staticmethod
    def unit_circle_to_dir(direction):
            return - (direction + 270) % 360

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction - degrees
        return self.direction

    def turn_right(self, degrees: int = 90):
        """Turns token by *degrees* degrees right

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction + degrees
        return self.direction

    def point_in_direction(self, direction) -> int:
        """
        Token points in given direction

        Args:
            direction: Direction the actor should point to

        Returns:
            The new direction as integer

        """
        direction = direction = self._value_to_direction(direction)
        self.direction = direction
        return self.direction

    def delta_x(self, distance):
        return round( math.sin(math.radians(self.direction)) * distance)

    def delta_y(self, distance):
        return - round(math.cos(math.radians(self.direction)) * distance)

    def point_towards_position(self, destination, center = False) -> int:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        if center is True:
            pos = self.rect.center
        else:
            pos = self.position
        x =  (destination[0] - pos[0])
        y =  (destination[1] - pos[1])
        if x != 0:
            m = y / x
        else:
            m = 0
            if destination[1] > self.position[1]:
                self.direction = 180
                return 180
            else:
                self.direction = 0
                return 0
        if destination[0] > self.position[0]:
            self.direction = 90 + math.degrees(math.atan(m))
        else:
            self.direction = 270 +  math.degrees(math.atan(m))
        return self.direction

    def point_towards_token(self, token) -> int:
        """
        Token points towards a given position

        Args:
            destination_position: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = token.rect.center
        return self.point_towards_position(pos, center = True)

    @direction.setter
    def direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        self.dirty = 1
        if self.costume:
            self.costume.call_action("rotate")
        if self.board:
            self.board.window.send_event_to_containers("actor_changed_direction", self)

    @property
    def size(self) -> tuple:
        """Size of the token

        """
        return self._size

    @size.setter
    def size(self, value :tuple):
        self._size = value
        self.dirty = 1
        if hasattr(self, "costume"):
            self.costume.call_action("scale")
        if hasattr(self, "physics") and self.physics:
            self.physics.dirty = 1

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def position(self) -> board_position.BoardPosition:
        """
        The position of the token is tuple (x, y)
        """
        return self._position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        self.last_position = self.position
        if type(value) == tuple:
            value = board_position.BoardPosition(value[0], value[1])
        self._position = value
        self.dirty = 1
        if self.board:
            self.board.window.send_event_to_containers("actor_moved", self)

    @property
    def x(self):
        """int: The x-value of an token
        """
        return self._position[0]

    @x.setter
    def x(self, value):
        self.position = (value, self.y)

    @property
    def y(self):
        """int: The x-value of an token
        """
        return self._position[1]

    @y.setter
    def y(self, value):
        self.position = (self.x, value)

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def center_x(self):
        return self.rect.centerx

    @property
    def center_y(self):
        return self.rect.centery

    @property
    def center(self) -> board_position.BoardPosition:
        return board_position.BoardPosition(self.center_x, self.center_y)

    @center_x.setter
    def center_x(self, value):
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value
        self.x = rect.topleft[0]

    @center_y.setter
    def center_y(self, value):
        rect = pygame.Rect.copy(self.rect)
        rect.centery = value
        self.y = rect.topleft[1]

    # Methoden
    def act(self):
        """Custom acting

        This method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def _value_to_direction(self, value) -> int:
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

    def remove(self):
        """Removes this actor from board
        """
        if self.board:
            self.board.remove_from_board(self)
        self.kill()
        del (self)

    def get_event(self, event, data):
        pass

    @classmethod
    def register_subclasses(base):
        d = {}
        for cls in base.__subclasses__():
            d[cls.__name__] = cls
        return d

    def start_physics(self):
        if self.physics:
            self.physics.start_physics()

    def setup_physics(self):
        self.physics = ph.PhysicsProperty()
        self.physics.token = self
        self.physics.can_move = True
        self.physics.shape_type = "rect"
        self.physics.gravity = True
        self.physics.mass = 1
        self.physics.elasticity = 0
        self.physics.stable = True
        self.physics.friction = 10

def is_position_on_board(self, position: board_position.BoardPosition) -> bool:
        """Tests if area or position is on board

        Args:
            position: A rectangle or a position

        Returns:
            true, if area is in grid

        """
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        if type(position) == board_position.BoardPosition:
            position = position.to_rect()

        top_left_x, top_left_y, right, top = position.topleft[0], \
                                             position.topleft[1], \
                                             position.right, \
                                             position.top
        if top_left_x < 0 or top_left_y < 0 or position.right >= self.width or position.bottom >= self.height:
            return False
        else:
            return True