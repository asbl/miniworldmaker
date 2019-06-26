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

    def __init__(self, position=None):
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
        self.last_position = (0, 0)
        self.last_direction = 90
        self.token_id = Token.token_count + 1
        self.is_static = False
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
            self.board = None
        self._dirty = 1

    @property
    def is_flipped(self):
        """
        If a token is flipped, it is mirrored via the y-axis.

        Returns:
            True, if token is flipped

        """
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
        """
        The image of the token:

        Warning: You should not draw on the image or similar,
        as the image will be reloaded during animations or other
        operations and changes will not be applied.

        Returns:
            The image of the token

        """
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
    def rect(self) -> pygame.Rect:
        """
        The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.

        Returns:
            The surrounding image

        """
        if self.dirty == 1:
            self._rect = self.position.to_rect(rect=self.image.get_rect())
            return self._rect
        else:
            return self._rect

    def add_image(self, path: str) -> int:
        """
        Adds an image to the token.
        Best Practice: Image should me placed in ./images subfolder of your project, because these images
        will be loaded before running the main-loop.

        Loading images is very slow, so this shouldn't be done in runtime.

        Args:
            path: Path to the images.

        Returns:
            The image index
        """
        image = self.costume.add_image(path)
        if not self.__class__.class_image:
            self.__class__.class_image = path
        return image

    def add_costume(self, path: str) -> costume.Costume:
        """
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            path: Path to the first image of new costume

        Returns:
            The new costume.

        """
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        new_costume.orientation = self.costume.orientation
        self.costumes.append(new_costume)
        return new_costume

    def switch_costume(self, index=-1) -> costume.Costume:
        """Switches the costume of token

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
        """
        Adds an actor to the board.
        Is called in __init__-Method if position is set.

        Args:
            board: The board, the actor should be added
            position: The position on the board where the actor should be added.
        """
        self.board = board
        self.position = position
        self.costume.changed_all()
        self.dirty = 1
        if self.init != 1:
            raise UnboundLocalError("Init was not called")
        self.board.window.send_event_to_containers("actor_created", self)
        self.set_token_mode()
        self.on_setup()

    def on_setup(self):
        """
        The setup()-Method is called after initialisation of object

        You can define own initialialisation operations here
        Returns:

        """
        pass

    def set_token_mode(self):
        from miniworldmaker.boards import pixel_board as pb
        from miniworldmaker.boards import tiled_board as tb
        if issubclass(self.board.__class__, pb.PixelBoard):
            cls = self.__class__
            self.__class__ = cls.__class__(PixelBoardToken.__name__, (cls, PixelBoardToken), {})
        elif issubclass(self.board.__class__, tb.TiledBoard):
            cls = self.__class__
            self.__class__ = cls.__class__(TiledBoardToken.__name__, (cls, TiledBoardToken), {})

    @property
    def direction(self) -> int:
        """ Sets direction the token is oriented

            0°:  East, x degrees clock-wise otherwise
            You can also set the direction by String ("forward", "up", "down", ...
        """
        return (self._direction + 180) % 360 - 180

    @property
    def direction_at_unit_circle(self):
        return Token.dir_to_unit_circle(self._direction)

    @direction_at_unit_circle.setter
    def direction_at_unit_circle(self, value):
        self.direction = Token.unit_circle_to_dir(value)

    @staticmethod
    def dir_to_unit_circle(direction):
        """
        Transforms the current direction into standard-unit-circle direction

        Args:
            value: The direction in scratch-style

        Returns:

        """
        return -(direction + 90) % 360 - 180

    @staticmethod
    def unit_circle_to_dir(direction):
        """
        Transforms the current direction from standard-unit-circle direction
        into scratch-style coordinates

        Args:
            value: The direction in math unit circle style.

        Returns:

        """
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

    def delta_x(self, distance):
        return round(math.sin(math.radians(self.direction)) * distance)

    def delta_y(self, distance):
        return - round(math.cos(math.radians(self.direction)) * distance)

    def point_towards_position(self, destination, center=True) -> int:
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
        x = (destination[0] - pos[0])
        y = (destination[1] - pos[1])
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
            self.direction = 270 + math.degrees(math.atan(m))
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
        return self.point_towards_position(pos, center=True)

    @property
    def size(self) -> tuple:
        """Size of the token

        """
        return self._size

    @size.setter
    def size(self, value: tuple):
        self._size = value
        self.dirty = 1
        if hasattr(self, "costume"):
            self.costume.call_action("scale")
        if hasattr(self, "physics") and self.physics:
            self.physics.dirty = 1

    @property
    def width(self):
        """
        The width of the token in pixels
        """
        return self.size[0]

    @property
    def height(self):
        """
        The height of the token in pixels
        """
        return self.size[1]

    @property
    def position(self) -> board_position.BoardPosition:
        """
        The position of the token as tuple (x, y)
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
        """x-value of token center-position"""
        return self.rect.centerx

    @property
    def center_y(self):
        """y-value of token center-position"""
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

    def move(self, distance: int = 0):
        """Moves actor *distance* steps.

        Args:
            distance: Number of steps to move.
            If distance = 0, the actor speed will be used.

        Returns:
            The actor

        Examples:

            >>> class Robot(Actor):
            >>>    def act(self):
            >>>         if self.sensing_on_board():
            >>>             self.move()
        """
        if distance == 0:
            distance = self.speed
        destination = self.get_destination(self.direction, distance)
        self.position = destination
        self.last_direction = self.direction
        return self

    def move_back(self):
        self.position = self.last_position
        self.direction = self.last_direction

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

    def move_in_direction(self, direction: Union[int, str]):
        """Moves actor *distance* steps into a *direction*.

        Args:
            direction: Direction as angle

        Returns:
            The actor

        """
        direction = self._value_to_direction(direction)
        self.direction = direction
        self.costume.is_rotatable = False
        self.move()
        return self

    def move_to(self, position: board_position.BoardPosition):
        """Moves actor *distance* steps into a *direction*.

        Args:
            position: The position to which the actor should move

        Returns:
            The actor

        """
        self.position = position
        return self

    def remove(self):
        """Removes this actor from board
        """
        if self.board:
            self.board.remove_from_board(self)
        if self.physics:
            self.physics.remove()
            self.physics = None
        self.kill()
        del (self)

    def get_event(self, event, data):
        pass

    def start_physics(self):
        """
        Starts the physics engine.
        The following values can be changed BEFORE calling this method:

        self.physics.can_move = True
        self.physics.shape_type = "rect"
        self.physics.gravity = True
        self.physics.mass = 1
        self.physics.elasticity = 0
        self.physics.stable = True
        self.physics.friction = 10

        """

        self.physics.start_physics()

    def setup_physics(self):
        """
        Setups physics engine. Is called with init and should be called BEFORE start_physics
        These are the standard-values:

        self.physics.token = self
        self.physics.can_move = True
        self.physics.shape_type = "rect"
        self.physics.gravity = True
        self.physics.mass = 1
        self.physics.elasticity = 0
        self.physics.stable = True
        self.physics.friction = 10
        """
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

    def flip_x(self) -> int:
        """Flips the actor by 180° degrees

        """
        if not self.costume.is_flipped:
            self.costume.is_flipped = True
        else:
            self.costume.is_flipped = False
        self.turn_left(180)
        return self.direction

    def get_destination(self, direction, distance) -> board_position.BoardPosition:
        x = self.position[0] + round(math.sin(math.radians(direction)) * distance)
        y = self.position[1] - round(math.cos(math.radians(direction)) * distance)
        return board_position.BoardPosition(x, y)

    def bounce_from_border(self, borders):
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        angle = self.direction
        if ("top" in borders and (
                (self.direction <= 0 and self.direction > -90 or self.direction <= 90 and self.direction >= 0))):
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
        else:
            pass
        return self

    def look(self, distance: int = 1) -> Union[board_position.BoardPosition, list]:
        """Looks *distance* steps into current direction

        Args:
            distance: Number of steps to look

        Returns:
            A destination Surface
        """
        pass

    def sensing_tokens(self, distance: int = -1, token_type=None, exact=False) -> list:
        """Checks if Actor is sensing Tokens in front

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise)
                instead of rectangles

        Returns:
            a list of tokens

        """
        pass

    def sensing_token(self, distance: int = -1, token_type=None, exact=False):
        """Checks if actor is sensing a single token in front. See sensing_tokens

        Args:
            distance: Number of steps to look for tokens  (0: at actor position)
            token_type: Class name of token types to look for. If token == None, all token are returned
            exact: If exact is True, then collision handling will be done with masks (slower, more precise) instead of rectangles

        Returns:
            A single token

        """
        pass

    def sensing_borders(self, distance: int = 1, ) -> list:
        """Checks if actor is sensing a border in front

        Args:
            distance: Number of steps to look for borders  (0: at actor position)

        Returns:
            a list of all borders ("top", "left", "right", "bottom") which are sensed on given position.

        """
        pass

    def sensing_on_board(self=None, distance=0) -> bool:
        """Checks if actor is sensing a position inside the board

        Args:
            distance: Number of steps to look for

        Returns:
            True if position is on board

        """
        pass

    def sensing_colors(self, distance: Union[int, None] = None, colors: Union[tuple, list] = []) -> set:
        """ Gets all colors the actor is sensing

        Args:
            distance: Number of steps to look for color

        Returns:
            All colors the actor is sensing as set

        """
        pass


class PixelBoardToken(Token):

    def get_target_rect(self, distance):
        target = self.get_destination(self.direction, distance)
        return target.to_rect(self.rect)

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(actor) == actor_type]

    def sensing_on_board(self=None, distance=0) -> bool:
        target_rect = self.get_target_rect(distance)
        topleft_on_board = board_position.BoardPosition(target_rect.left, target_rect.top).is_on_board()
        bottom_right_on_board = board_position.BoardPosition(target_rect.right, target_rect.bottom).is_on_board()
        return topleft_on_board and bottom_right_on_board

    def sensing_borders(self, distance: int = 1, ) -> list:
        for i in range(distance + 1):
            target_rect = self.get_target_rect(distance)
            borders = self.board.borders(target_rect)
            if borders:
                self.board.window.send_event_to_containers("actor_is_looking_at_border", self)
                return borders
        else:
            return []

    def sensing_tokens(self, distance: int = 1, token_type=None, exact=False) -> list:
        pass

    def sensing_token(self, distance: int = 1, token_type=None, exact=False) -> Union[Token, None]:
        destination_rect = self.get_target_rect(distance)
        token = self.board.get_tokens_in_area(destination_rect, singleitem=True, exclude=self, token_type=token_type)
        if exact and token:
            if pygame.sprite.collide_mask(self, token):
                return token
            else:
                return None
        return None

    def look(self, distance: int = 1) -> Union[board_position.BoardPosition, list]:
        direction = self.direction
        return self.get_line(direction, distance)

    def get_line(self, direction, distance):
        line = []
        i = 0
        while i < distance:
            position = self.rect.center
            x = position[0] + round(math.sin(math.radians(direction)) * i)
            y = position[1] - round(math.cos(math.radians(direction)) * i)
            pos = board_position.BoardPosition(x, y)
            if not self.rect.collidepoint(pos[0], pos[1]):
                line.append(pos)
            else:
                distance += 1
            i += 1
        return line

    def sensing_colors(self, distance: Union[int, None] = None, colors: Union[tuple, list] = ()) -> list:
        if distance is None:
            distance = self.speed
        line = self.look(distance=distance)
        colorlist = self.board.get_colors_at_line(line)
        # if type is tupel, transform into list
        if type(colors) == tuple:
            colors = [colors]
        if not colors:
            return colorlist
        intersections = [value for value in colorlist if value in colors]
        return intersections

    def bounce_from_token(self, token):
        """experimental: Bounces actor from another token
        Args:
            token: the token

        Returns: the actor

        """
        angle = self.direction
        self.move(-self.speed)
        self.point_towards_token(token)
        incidence = self.direction - angle
        self.turn_left(180 - incidence)
        return self


class TiledBoardToken(Token):

    def sensing_on_board(self=None, distance=0) -> bool:
        target = self.get_destination(self.direction, distance)
        on_board = target.is_on_board()
        return on_board

    def sensing_tokens(self, distance: int = 1, token_type=None, exact=False) -> list:
        target = self.get_destination(self.direction, distance)
        return self.board.get_tokens_at_position(target, token_type, exclude=self)

    def sensing_token(self, distance: int = 1, token_type=None, exact=False) -> list:
        target = self.get_destination(self.direction, distance)
        return self.board.get_tokens_at_position(target, token_type, exclude=self, singleitem=True)
