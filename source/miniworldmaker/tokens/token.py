from __future__ import annotations
import math
from typing import Tuple, Union, Type, TypeVar, List, Optional, Tuple
import pygame
from miniworldmaker.appearances import appearance
from miniworldmaker.appearances import costume
from miniworldmaker.board_positions import board_position
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError, TokenArgumentShouldBeTuple, NotImplementedOrRegisteredError
import miniworldmaker
from miniworldmaker.tools import token_inspection

class Meta(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = super().__call__(*args, **kwargs)
        except NoValidBoardPositionError:
            raise TokenArgumentShouldBeTuple()
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board(instance._position)
        return instance


class Token(pygame.sprite.DirtySprite, metaclass=Meta):
    """Tokens are objects on your board. Tokens can :doc:`move <../key_concepts/movement>` around the board and have :doc:`sensors <../key_concepts/sensors>` to detect other tokens.

    The appearance of a token is determined by its :doc:`Costume <../key_concepts/costumes>`.

    These are the Token Types you can use:

    * Token: Base class for all Kinds of Tokens
    * TextToken: A TextToken
    * NumberToken: A NumberToken
    * Rectangle: A Rectangle
    * Line: A Line
    * Circle: A Circle

    Examples:

        Creating a token:

        .. code-block:: python

          board = miniworldmaker.PixelBoard()
          board.size = (800,300)
          my_token = miniworldmaker.Token(position=(0, 0))

        Creating a token Class:

        .. code-block:: python

          class MyToken(miniworldmaker.Token):
              def on_setup(self):
                  self.add_costume("images/2.png")

          my_token = MyToken(position = (40,130))

        Creating a Circle from Center at mouse position

        .. code-block:: python

          miniworldmaker.Circle.from_center(self.get_mouse_position(), 80, 1, (200,200,200,100))

    See Also:

        * See: :doc:`Token <../api/token>`
        * See: :doc:`Shapes <../api/token.shape>`
        * See: :doc:`TextTokens and NumberTokens <../api/token.texttoken>`
    Args:
        position: The topleft position of the token as tuple,. e.g. (200,200)
        image: path to an image which should be used as costume, e.g. ("images/my_costume.png")

    Attributes:

        collision_type (string):
            The attribute collision_type specifies how collisions should be checked:

            * "default": tile for TiledBoards, 'maask' for PixelBoards

            * "tile": Are tokens on the same tile? (only TiledBoard)

            * "rect": Are tokens colliding when checking their bounding - boxes? (Only PixelBoard)

            * "static-rect": Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

            * "circle": Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

            * "mask": Are tokens colliding when checkig if their image masks are overlapping.
    """
    token_count: int = 0
    class_image: str = ""

    def __init__(self, position: Optional[Union[Tuple, "miniworldmaker.BoardPosition"]] = None,
                 image: Optional[str] = None, static=False):
        self._managers: list = list()
        self.token_id: int = Token.token_count + 1
        self.costume_manager: miniworldmaker.TokenCostumeManager = None
        self.board_sensor: miniworldmaker.TokenBoardSensor = None
        self.position_manager: miniworldmaker.TokenPositionManager = None
        self.board: miniworldmaker.Board = miniworldmaker.App.board
        _token_connector = self.board.get_token_connector(self)
        _token_connector.add_token_managers(image, position)
        pygame.sprite.DirtySprite.__init__(self)
        Token.token_count += 1
        self.speed: int = 1
        self.collision_type: str = ""
        self._layer : int = 0
        self.static : bool = static
        self._position: "board_position.BoardPosition"= position

    @property
    def layer(self) -> int:
        return self._layer

    @layer.setter
    def layer(self, value: int):
        self._layer = value
        self.board._tokens.change_layer(self, value)

    @property
    def last_position(self) -> "board_position.BoardPosition":
        return self.position_manager.last_position

    @property
    def last_direction(self) -> int:
        return self.position_manager.last_direction

    @classmethod
    def from_center(cls, center_position: "board_position.BoardPosition"):
        """
        Creates a token with center at center_position

        Args:
            center_position: Center of token
        """
        obj = cls(position=(0, 0))  # temp positition
        obj.center = center_position  # pos set to center
        return obj

    @property
    def costume_count(self) -> int:
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

        Returns:
            int: The new direction

        Examples:

            flip a token.

            >>>  def on_sensing_not_on_board(self):
            >>>    self.move_back()
            >>>    self.flip_x()
        """
        return self.position_manager.flip_x()

    def __str__(self):
        if self.board:
            return "{0}-Object, ID: {1} at pos {2} with size {3}".format(self.class_name, self.token_id, self.position,
                                                                         self.size)
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
    def dirty(self) -> int:
        """If token is dirty, it will be repainted.

        Returns:
            int: 1 if token is dirty/0 otherwise
        """
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

    def get_rect(self) -> pygame.Rect:
        return self.position_manager.rect

    def add_costume(self, source=(255, 255, 0, 0)) -> costume.Costume:
        """Adds a new costume to token.
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

    def switch_costume(self, costume: Union[int, Type["appearance.Appearance"]]) -> "costume.Costume":
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
    def costume(self) -> costume.Costume:
        return self.costume_manager.costume

    @costume.setter
    def costume(self, value):
        self.costume_manager.costume = value

    @property
    def costumes(self):
        return self.costume_manager.costumes

    @property
    def orientation(self) -> int:
        return self.costume.orientation

    @orientation.setter
    def orientation(self, value: int):
        self.costume.orientation = value

    @property
    def direction(self) -> int:
        """Directions are handled exactly as in the Scratch programming language, 
        see: `Scratch Wiki <https://en.scratch-wiki.info/wiki/Direction_(value)>`_ 

        The default direction is 0°. All tokens are looking "up"

        .. image:: /_images/movement.jpg
            :width: 100%
            :alt: Move on board

        **Values for Direction**

        * 0° or "up": up
        * 90° or "right": Move right
        * -90° or "left": Move left
        * 180° or "down": Move down
        * "forward": Current direction



        Sets direction of the token.

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
    def x(self, value: float):
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

    def move_up(self, distance: int = 1):
        return self.position_manager.move_in_direction("up", distance)

    def move_down(self, distance: int = 1):
        return self.position_manager.move_in_direction("down", distance)

    def move_left(self, distance: int = 1):
        return self.position_manager.move_in_direction("left", distance)

    def move_right(self, distance: int = 1):
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
        if hasattr(self, "board") and self.board:
            self.board.remove_from_board(self)
        for manager in self._managers:
            manager.remove()
            del (manager)
        self.kill()
        del (self)

    @property
    def is_rotatable(self) -> bool:
        return self.costume.is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value: bool):
        self.costume.is_rotatable = value

    def bounce_from_border(self, borders: List[str]) -> Token:
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The token

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

    def sensing_tokens(self, token_filter: str = None, distance: int = 0, collision_type: str = "default") -> List[Token]:
        """Senses if tokens are on tokens position.
        Returns a list of tokens.

        .. image:: ../_images/sensing_tokens.png

        Args:
            token_filter: filter by token type. Enter a class_name of tokens to look for here
            distance: Specifies the distance in front of the actuator to which the sensor reacts.
            collision_type: The type of collision which should be checked:

        Returns:
            All tokens found by Sensor

        """
        return self.board_sensor.sensing_tokens(token_filter, distance)

    def sensing_token(self, token_filter: Union[str, "Token"] = None, distance: int = 0, collision_type: str = "default") -> List[Token]:
        """Senses if tokens are on tokens position.
        Returns the first found token.

        .. image:: ../_images/sensing_token.png

        Args:
            token_filter: filter by token type or by token instance
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
        return self.board_sensor.sensing_token(token_filter, distance)

    def sensing_borders(self, distance: int = 0) -> bool:
        """
        Senses borders

        .. image:: ../_images/sensing_borders.png

        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns:
            True if border was found.

        """
        return self.board_sensor.sensing_borders(distance)

    def sensing_left_border(self, distance: int = 0) -> bool:
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "left" in self.board_sensor.sensing_borders(distance)

    def sensing_right_border(self, distance: int = 0) -> bool:
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "right" in self.board_sensor.sensing_borders(distance)

    def sensing_top_border(self, distance: int = 0) -> bool:
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "top" in self.board_sensor.sensing_borders(distance)

    def sensing_bottom_border(self, distance: int = 0) -> bool:
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return "bottom" in self.board_sensor.sensing_borders(distance)

    def sensing_colors(self, colors: Tuple, distance: int) -> tuple:
        """
        Senses colors in board-background at token-position

        Args:
            colors:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: All colors found by Sensor

        """
        colors = self.board_sensor.sensing_colors(colors, distance)
        return colors

    def sensing_point(self, board_position: Union["board_position.Boardposition", Tuple]) -> bool:
        """
        Is the token colliding with a specific (global) point?

        Returns: True if point is below token
        """
        return self.rect.collidepoint(board_position)

    def register(self, method: callable):
        """This method is used for the @register decorator. It adds a method to an object

        Args:
            method (callable): The method which should be added to the token
        """
        bound_method = token_inspection.TokenInspection(self).bind_method(method)
        if method.__name__ == "on_setup":
            self.on_setup()
        self.board.event_handler.register_event(method.__name__, self)
        return bound_method

    def bounce_from_token(self, other: "Token"):
        self.position_manager.bounce_from_token(other)

    def animate(self, speed: int = 10):
        self.costume_manager.animate(speed)

    def animate_costume(self, costume: costume.Costume, speed: int = 10):
        self.costume_manager.animate_costume(costume, speed)

    def loop_animation(self, speed: int = 10):
        self.costume_manager.loop_animation(speed)

    def send_message(self, message: str):
        self.board.app.event_manager.send_event_to_containers(
            "message", message)

    def on_key_down(self, key: list):
        """**on_key_down**  is called one time when a key is pressed down.

        Instead of **on_key_down** you can use **on_key_down_letter**, e.g. **on_key_down_a** or **on_key_down_w**
        , if you want to handle a on_key_down event for a specific letter.

        Examples:

        Register a key_down event:

        .. code-block::

            token1 = miniworldmaker.Token(position = (2, 2) )
            token1.add_costume((100,0,100,100))

            @token1.register
            def on_key_down(self, key):
                print(key)

        Register on_key_down_a event

        .. code-block::

            token1 = miniworldmaker.Token(position = (2, 2) )
            token1.add_costume((100,0,100,100))

            @token1.register
            def on_key_down_a(self):
                print("a")

        Args:
            key (list): The typed key as list (e.g. ['A', 'a']) containing both uppercase and lowercase of typed letter.

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_key_pressed(self, key: list):
        """**on_key_pressed** is called when while key is pressed. If you hold the key, on_key_pressed 
        is repeatedly called again and again until the key is released.

        Like `on_key_down` the method can be called in the variant `on_key_pressed_[letter]` (e.g. `on_key_pressed_w(self)`). 

        Examples:

            Register on_key_pressed event:

            .. code-block::

                token1 = miniworldmaker.Token(position = (2, 2) )
                token1.add_costume((100,0,100,100))

                @token1.register
                def on_key_pressed(self, key):
                    print("pressed", key)

                @token1.register
                def on_key_pressed_s(self):
                    print("pressed s")

        Args:
            key (list): The typed key as list (e.g. ['C', 'c', 'D', 'd']) containing both uppercase and lowercase of typed letter.

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_key_up(self, key):
        raise NotImplementedOrRegisteredError()

    def on_mouse_left(self, position: tuple):
        """Method is called when left mouse button was pressed.


        Examples
            Register mouse event to board

            .. code-block::

                @board.register
                def on_mouse_left(self, position):
                    print("left" + str(position))

                @board.register
                def on_mouse_right(self, position):
                    print("right" + str(position))

                @board.register
                def on_mouse_middle(self, position):
                    print("middle" + str(position))


        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """

        raise NotImplementedOrRegisteredError()

    def on_mouse_right(self, position: tuple):
        """on_mouse_right is called when right mouse button was pressed.

        Examples

            Register mouse event to board

            .. code-block::

                @board.register
                def on_mouse_right(self, position):
                    print("right" + str(position))

        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_mouse_motion(self, position: tuple):
        """on_mouse_motion is called when right mouse moves.

        Examples

            Register mouse-motion event to board

            .. code-block::

                @board.register
                def on_mouse_motion(self, position):
                    print("motion" + str(position))

        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_message(self, message: str):
        """Messages are used to allow objects to communicate with each other.

        Send a message:

        * A token and the board can send a message to all tokens and the board with the command: self.send_message(“message_string”)

        Process a message:

        * If your board or your token should react to messages you can use the event on_message:

        Examples:

            Receive a message

            .. code-block::

                @player.register
                def on_message(self, message):
                    if message == "Example message":
                    do_something()

        Args:
            message (str): The message as string

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_clicked_left(self, position: tuple):
        """The mouse is on top of a token and mouse was clicked.

        Examples:

            Registering a on_click event:

            .. code-block::

                token = miniworldmaker.Token((2,2))

                @token.register
                def on_clicked_left(self, position):
                    print("clicked" + str(position))


        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_clicked_right(self, position):
        """The mouse is on top of a token and mouse was clicked.

        Examples:

            Registering a on_click event:

            .. code-block::

                token = miniworldmaker.Token((2,2))

                @token.register
                def on_clicked_right(self, position):
                    print("clicked" + str(position))


        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_sensing_on_board(self):
        """*on_sensing_on_board* is called, when token is on board"

        Examples:

            Register on_sensing_on_board method:

            .. code-block::

                @player.register
                    def on_sensing_on_board(self):
                    print("Player 3: I'm on the board:")

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.

        """
        raise NotImplementedOrRegisteredError()

    def on_sensing_not_on_board(self):
        """*on_sensing_not_on_board* is called, when token is not on board"

        Examples:

            Register on_sensing_not_on_board method:

            .. code-block::

                @player.register
                    def on_sensing_not_on_board(self):
                    print("Warning: I'm not on the board!!!")

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_sensing_borders(self, str: List(str)):
        """*on_sensing_border* is called, when token is near a border

        Args:
            str (List): A list of strings with found borders, e.g.: ['left', 'top']

        Examples:

            Register on_sensing_border_event: 

            .. code-block::

                @player.register
                def on_sensing_borders(self, borders):
                    print("Player 4: Sensing borders:")
                    print("Borders are here!", str(borders))

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def on_sensing_token(self, token: "Token"):
        """*on_sensing_token* is called, when token is sensing a token on same position

        Args:
            token (Token): The found token

        Examples:

            Register sensing_token event 

            .. code-block::

                @player.register
                def on_sensing_token(self, token):
                    print("Player 1: Sensing token:")
                    if token == player2:
                    print("Am i sensing player2?" + str(token == player2))

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()
