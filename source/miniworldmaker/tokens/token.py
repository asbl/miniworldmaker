import math
from typing import Tuple, Union, Type, TypeVar, List, Optional, Tuple
import pygame
from miniworldmaker.app import app
from miniworldmaker.appearances.appearance import Appearance
from miniworldmaker.appearances import costume
from miniworldmaker.board_positions import board_position
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError, TokenArgumentShouldBeTuple
from miniworldmaker.tokens.physics import token_physics
from miniworldmaker.tools import inspection_methods
from miniworldmaker.tools import binding

T = TypeVar('T')
appearance_source = Union[str, List[str], Appearance]


class Meta(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = super().__call__(*args, **kwargs)
        except NoValidBoardPositionError:
            raise TokenArgumentShouldBeTuple()
        if instance.costume:
            instance.costume._reload_all()
        if inspection_methods.InspectionMethods.has_parent_with_name(app.App.board, "PhysicsBoard") or inspection_methods.InspectionMethods.has_class_name(app.App.board, "PhysicsBoard"):
            instance.physics = token_physics.TokenPhysics(
                instance, app.App.board)
            if hasattr(instance, "set_physics_default_values"):
                instance.set_physics_default_values()
        if hasattr(instance, "on_setup"):
            instance.on_setup()
        if hasattr(instance, "setup"):
            instance.setup()
        if inspection_methods.InspectionMethods.has_parent_with_name(app.App.board, "PhysicsBoard") or inspection_methods.InspectionMethods.has_class_name(app.App.board, "PhysicsBoard"):
            instance.physics.start()
            instance.board.physics_tokens.append(instance)
            if hasattr(instance, "on_begin_simulation"):
                instance.on_begin_simulation()
        return instance


class Token(pygame.sprite.DirtySprite, metaclass=Meta):
    """
    Token is the basic class for all kinds of players,
    pieces and obstacles on the playing field

    Attributes:
    
        collision_type (string):
            The parameter collision_type specifies how collisions should be checked:

                * "default": tile for TiledBoards, 'maask' for PixelBoards

                * "tile": Are tokens on the same tile? (only TiledBoard)

                * "rect": Are tokens colliding when checking their bounding - boxes? (Only PixelBoard)

                * "static-rect": Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

                * "circle": Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

                * "mask": Are tokens colliding when checkig if their image masks are overlapping.
        """
    token_count = 0
    class_image = None
    subclasses = None

    def __init__(self, position: Optional[Union[Tuple, "board_position.BoardPosition"]] = None, image: Optional[str] = None):
        self._managers = list()
        self.token_id: int = Token.token_count + 1
        self.costume_manager = None
        self.board_sensor = None
        self.position_manager = None
        self.method_manager = None
        self.board = app.App.board
        _token_connector = self.board.get_token_connector(self)
        _token_connector.add_token_managers(image, position)
        pygame.sprite.DirtySprite.__init__(self)
        _token_connector.add_token_to_board(self.position)
        Token.token_count += 1
        self.speed: int = 1
        self.collision_type: str = ""
        self._layer = 0

    @property 
    def layer(self):
        return self._layer

    @layer.setter 
    def layer(self, value):
        self._layer = value
        self.board._tokens.change_layer(self, value)


    @property
    def last_position(self):
        return self.position_manager.last_position

    @property
    def last_direction(self):
        return self.position_manager.last_direction

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
    def costume_count(self):
        return self.costume_manager.costume_count

    @property
    def is_flipped(self) -> bool:
        """
        If a token is flipped, it is mirrored via the y-axis.

        Returns:
            True, if token is flipped

        Examples:

            flip a token in Example flipthefish.py

            >>>  def on_sensing_not_on_board(self):
            >>>    self.move_back()
            >>>    self.flip_x()
        """
        return self.costume.is_flipped

    @is_flipped.setter
    def is_flipped(self, value: bool):
        self.costume_manager.flip_costume(value)

    def flip_x(self) -> int:
        """Flips the actor by 180° degrees

        .. image:: ../_images/flip_x.png

        Examples:

            flip a token.

            >>>  def on_sensing_not_on_board(self):
            >>>    self.move_back()
            >>>    self.flip_x()
        """

        return self.position_manager.flip_x()

    def __str__(self):
        if self.board:
            return "{0}-Object, ID: {1} at pos {2} with size {3}".format(self.class_name, self.token_id, self.position, self.size)
        else:
            return "**: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        """
        The image of the token:

        > Warning: You should not directly draw on the image
        > as the image will be reloaded during animations 

        """
        return self.costume_manager.image

    @property
    def dirty(self):
        if self.costume_manager:
            return self.costume_manager.dirty

    @dirty.setter
    def dirty(self, value: int):
        if self.costume_manager:
            self.costume_manager.dirty = value

    @property
    def rect(self) -> pygame.Rect:
        """
        The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.
        """
        return self.position_manager.rect

    def get_rect(self):
        return self.position_manager.rect

    def add_costume(self, source: appearance_source = (255, 255, 0, 0)) -> costume.Costume:
        """    def register(self, method: callable):
        bound_method = method.__get__(self, self.__class__)
        setattr(self, method.__name__, bound_method)
        if method.__name__ == "on_setup":
            self.on_setup()
        return bound_method
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            path: Path to the first image of new costume

        Returns:
            The new costume.

        """
        return self.costume_manager.add_costume(source)

    def remove_costume(self, costume: int = None):
        """Removes a costume from token

        Args:
            index: The index of the new costume. Defaults to -1 (last costume)
        """
        self.costume_manager.remove_costume(costume)

    def switch_costume(self, costume: Union[int, Type[Appearance]]) -> costume.Costume:
        """Switches the costume of token

        Args:
            next: If next is True, the next costume will be selected

        Returns: The new costume
        """
        self.costume_manager.switch_costume(costume)

    def next_costume(self):
        """Switches to the next costume of token

        Args:
            next: If next is True, the next costume will be selected

        Returns: The new costume
        """
        self.costume_manager.next_costume()

    @property
    def costume(self):
        return self.costume_manager.costume

    @costume.setter
    def costume(self, value):
        self.costume_manager.costume = value

    @property
    def costumes(self):
        return self.costume_manager.costumes

    @property
    def orientation(self):
        return self.costume.orientation

    @orientation.setter
    def orientation(self, value):
        self.costume.orientation = value

    @property
    def direction(self) -> int:
        """ Sets direction of the token.

        You can use a integer or a string to describe the direction

        Options
            * 0, "up" - Look up
            * 90, "right", - Look right
            * -90, "left", - Look left
            * -180, 180, "down" - Look down

        .. image:: ../_images/direction.png

        Examples:

            Move in a direction with WASD-Keys

            >>> def on_key_down(self, keys):
            >>>    if "W" in keys:
            >>>      self.direction = "up"
            >>>    elif "S" in keys:
            >>>      self.direction = "down"
            >>>    elif "A" in keys:
            >>>      self.direction = "left"
            >>>    elif "D" in keys:
            >>>      self.direction = "right"
            >>>    self.move()


        """
        return self.position_manager.direction

    @direction.setter
    def direction(self, value: int):
        self.position_manager.direction = value

    @property
    def direction_at_unit_circle(self) -> int:
        """
        Gets the direction as value in unit circle (0° right, 90° top, 180° left...
        """
        return self.position_manager.dir_to_unit_circle(self.direction)

    @direction_at_unit_circle.setter
    def direction_at_unit_circle(self, value: int):
        """
        Sets the direction from unit circle
        Args:
            value: An angle in the unit circle, e.g. 0°: right, 90° top, ...
        """
        self.direction = self.position_manager.unit_circle_to_dir(value)

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        .. image:: ../_images/turn_left.png

        Options:
          * You can set the value token.is_rotatable = False if you don't want the token to be rotated.

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        return self.position_manager.turn_left(degrees)

    def turn_right(self, degrees: int = 90):
        """Turns token by *degrees* degrees right

        .. image:: ../_images/turn_right.png

        Options:
          * You can set the value token.is_rotatable = False if you don't want the token to be rotated.

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        return self.position_manager.turn_right(degrees)

    def point_in_direction(self, direction: int) -> int:
        """Token points in given direction.

        You can use a integer or a string to describe the direction

        Args:
            The direction as integer or string (see options)

        Options
            * 0, "up" - Look up
            * 90, "right", - Look right
            * -90, "left", - Look left
            * -180, 180, "down" - Look down

        .. image:: ../_images/direction.png

        Examples:

            Move in a direction with WASD-Keys

            >>> def on_key_down(self, keys):
            >>>    if "W" in keys:
            >>>      self.direction = "up"
            >>>    elif "S" in keys:
            >>>      self.direction = "down"
            >>>    elif "A" in keys:
            >>>      self.direction = "left"
            >>>    elif "D" in keys:
            >>>      self.direction = "right"
            >>>    self.move()
        """
        return self.position_manager.point_in_direction(direction)

    def delta_x(self, distance: int) -> int:
        return math.sin(math.radians(self.direction)) * distance

    def delta_y(self, distance: int) -> int:
        return - math.cos(math.radians(self.direction)) * distance

    def point_towards_position(self, destination: int) -> int:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        Examples:

            Point towards mouse_position:

            >>>  def act(self):
            >>>  mouse = self.board.get_mouse_position()
            >>>  if mouse:
            >>>    self.point_towards_position(mouse)
            >>>  self.move()
        """
        return self.board_sensor.point_towards_position(destination)

    def point_towards_token(self, other: "Token") -> int:
        """
        Token points towards another token.

        Args:
            other: The other token

        Returns:
            The new direction

        """
        pos = other.rect.center
        return self.point_towards_position(pos)

    @property
    def size(self) -> tuple:
        """Size of the token

        """
        return self.position_manager.size

    @size.setter
    def size(self, value: tuple):
        self.set_size(value)

    def set_size(self, value: tuple):
        self.position_manager.size = value

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
        The position of the token as BoardPosition (x, y)
        """
        return self.position_manager.position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        self.position_manager.position = value

    @property
    def x(self) -> float:
        """int: The x-value of an token
        """
        return self.position_manager.x

    @x.setter
    def x(self, value) -> float:
        self.position_manager.x = value

    @property
    def y(self) -> float:
        """int: The x-value of an token
        """
        return self.position_manager.y

    @y.setter
    def y(self, value: float):
        self.position_manager.y = value

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def center_x(self):
        """x-value of token center-position"""
        return self.position_manager.center_x

    @property
    def topleft_x(self):
        """x-value of token topleft-position"""
        return self.rect.topleft[0]

    @property
    def topleft_y(self):
        """x-value of token topleft-position"""
        return self.rect.topleft[1]

    @property
    def topleft(self) -> board_position.BoardPosition:
        return self.position_manager.topleft

    @topleft.setter
    def topleft(self, value: Union[Tuple, board_position.BoardPosition]):
        self.position_manager.topleft = value

    @property
    def center_y(self):
        """y-value of token center-position"""
        return self.position_manager.center_y

    @property
    def center(self) -> board_position.BoardPosition:
        return self.position_manager.center

    @center_x.setter
    def center_x(self, value: float):
        self.position_manager.center_x = value

    @center_y.setter
    def center_y(self, value: float):
        self.position_manager.center_y = value

    @center.setter
    def center(self, value: Union[Tuple, board_position.BoardPosition]):
        self.position_manager.center = value

    def move(self, distance: int = 0):
        """Moves actor *distance* steps in current direction

        .. image:: ../_images/move.png

        Args:
            distance: Number of steps to move.
              If distance = 0, the actor speed will be used.

        Returns:
            The moved token

        Examples:

            if sensing_on_board, move forward:

            >>> class Robot(Token):
            >>>    def act(self):
            >>>         if self.sensing_on_board():
            >>>             self.move()
        """
        return self.position_manager.move(distance)

    def move_up(self, distance : int = 1):
        return self.position_manager.move_in_direction("up", distance)

    def move_down(self, distance : int = 1):
        return self.position_manager.move_in_direction("down", distance)

    def move_left(self, distance : int = 1):
        return self.position_manager.move_in_direction("left", distance)

    def move_right(self, distance : int = 1):
        return self.position_manager.move_in_direction("right", distance)

    def move_back(self):
        """
        "Undo" the last move. Moves the actor to the last position and resets direction.

        .. image:: ../_images/move_back.png

        Returns:
            The moved token

        Examples:

            move_back when field is blocked:

            >>>  def on_sensing_wall(self, wall):
            >>>    self.move_back()

        """
        return self.position_manager.move_back()

    def move_in_direction(self, direction: Union[int, str], distance=1):
        """Moves token *distance* steps into a *direction*.

        .. image:: ../_images/move_in_direction.png

        Options
            * 0, "up" - Look up
            * 90, "right", - Look right
            * -90, "left", - Look left
            * -180, 180, "down" - Look down

        .. image:: ../_images/direction.png

        Args:
            direction: Direction as angle

        Returns:
            The token itself

        """
        return self.position_manager.move_in_direction(direction, distance)

    def move_to(self, position: board_position.BoardPosition):
        """Moves token *distance* to a specific board_posiition

        Args:
            position: The position to which the actor should move. The position can be a 2-tuple (x, y)
            which will be converted to a board_position

        .. image:: ../_images/move_to.png

        Returns:
            The token itself

        Examples:

        move to (3, 2) on mouse_click

        >>> def on_clicked_left(self, position):
        >>>   self.move_to((3,2))


        """
        return self.position_manager.move_to(position)

    def remove(self):
        """
        Removes this token from board

        Examples:

            Removes robots in thecrash.py :

            >>>    def act(self):
            >>>        self.move()
            >>>        other = self.sensing_token(distance = 0, token_type=Robot)
            >>>    if other:
            >>>        explosion = Explosion(position=self.position)
            >>>        self.remove()
            >>>        other.remove()
        """
        for manager in self._managers:
            manager.remove()
            del(manager)
        self.kill()
        del (self)

    @property
    def is_rotatable(self):
        return self.costume.is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self.costume.is_rotatable = True

    def bounce_from_border(self, borders: List):
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        return self.position_manager.bounce_from_border(borders)

    def sensing_on_board(self, distance: int = 0) -> bool:
        """
        Is the token on board if it is moving distance steps forward?

        .. image:: ../_images/sensing_on_board.png

        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns:
            True if token is on board

        """
        return self.board_sensor.sensing_on_board(distance=distance)

    def sensing_tokens(self, token_type: str = None, distance: int = 0, collision_type: str = "default"):
        """Senses if tokens are on tokens position.
        Returns a list of tokens.

        .. image:: ../_images/sensing_tokens.png

        Args:
            token_type: filter by token type. Enter a class_name of tokens to look for here
            distance: Specifies the distance in front of the actuator to which the sensor reacts.
            collision_type: The type of collision which should be checked:

        Returns:
            All tokens found by Sensor

        """
        return self.board_sensor.sensing_tokens(token_type, distance)

    def sensing_token(self, token_type: str = None, distance: int = 0, collision_type: str = "default"):
        """Senses if tokens are on tokens position.
        Returns the first found token.

        .. image:: ../_images/sensing_token.png

        Args:
            token_type: filter by token type. Enter a class_name of tokens to look for here
            distance: Specifies the distance in front of the actuator to which the sensor reacts.
            collision_type: The type of collision which should be checked:

        Returns:
            First token found by Sensor

        Examples:
            Sensing a fireplace in rpg.py:

            >>>  fireplace =  self.player.sensing_token(Fireplace)
            >>>    if fireplace:
            >>>      self.console.newline("Du zündest die Feuerstelle an.")
            >>>      self.fireplace.burn()

        """
        return self.board_sensor.sensing_token(token_type, distance)

    def sensing_borders(self, distance: int = 0):
        """
        Senses borders

        .. image:: ../_images/sensing_borders.png

        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns:
            True if border was found.

        """
        return self.board_sensor.sensing_borders(distance)

    def sensing_left_border(self, distance: int = 0):
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "left" in self.board_sensor.sensing_borders(distance)

    def sensing_right_border(self, distance: int = 0):
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "right" in self.board_sensor.sensing_borders(distance)

    def sensing_top_border(self, distance: int = 0):
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "top" in self.board_sensor.sensing_borders(distance)

    def sensing_bottom_border(self, distance: int = 0):
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "bottom" in self.board_sensor.sensing_borders(distance)

    def sensing_colors(self, colors: Tuple, distance: int):
        """
        Senses colors in board-background at token-position

        Args:
            colors:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: All colors found by Sensor

        """
        colors = self.board_sensor.sensing_colors(colors, distance)
        return colors

    def sensing_point(self, board_position: Union["board_position.Boardposition", Tuple]):
        """
        Is the token colliding with a specific (global) point?

        Returns: True if point is below token
        """
        return self.rect.collidepoint(board_position)

    """ 
    This method is used for the @register decorator. It adds a method to an object
    """

    def register(self, method: callable):
        bound_method = binding.bind_method(self, method)
        if method.__name__ == "on_setup":
            self.on_setup()
        return bound_method

    def bounce_from_token(self, other: "Token"):
        self.position_manager.bounce_from_token(other)

    def animate(self, speed: int = 10):
        self.costume_manager.animate(speed)

    def animate_costume(self, costume: "costume.Costume", speed: int = 10):
        self.costume_manager.animate_costume(costume, speed)

    def loop_animation(self, speed: int = 10):
        self.costume_manager.loop_animation(speed)

    def send_message(self, message: str):
        self.board.app.event_manager.send_event_to_containers(
            "message", message)
