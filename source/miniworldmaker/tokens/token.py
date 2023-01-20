from __future__ import annotations

from typing import Union, List, Tuple, Optional, cast

import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.costume as costume_mod
import miniworldmaker.appearances.costumes_manager as costumes_manager
# from miniworldmaker.tokens.sensors import token_boardsensor - @todo not imported because of circular import
import miniworldmaker.dialogs.ask as ask
import miniworldmaker.positions.direction as board_direction
import miniworldmaker.positions.position as board_position
import miniworldmaker.tokens.managers.token_position_manager as token_position_manager
import miniworldmaker.tokens.token_base as token_base
import miniworldmaker.tools.token_inspection as token_inspection
import pygame.rect
from miniworldmaker.exceptions.miniworldmaker_exception import (
    MiniworldMakerError,
    NotImplementedOrRegisteredError,
    NoBoardError,
    RegisterError,
    NoValidBoardPositionError,
    MissingBoardSensor,
    MissingPositionManager
)


class Meta(type):
    def __call__(cls, *args, **kwargs):
        if len(args) >= 2 and type(args[0]) == int and type(args[1]) == int:
            first = (args[0], args[1])
            last_args = [args[n] for n in range(2, len(args))]
            args = [first] + last_args
        instance = type.__call__(cls, *args, **kwargs)  # create a new Token
        _token_connector = instance.board.get_token_connector(instance)
        _token_connector.add_token_to_board()
        return instance


class Token(token_base.BaseToken):
    """Tokens are objects on your board. Tokens can move around the board and have sensors to detect other tokens.

    The appearance of a token is determined by its costume.

    Examples:

        Create a token:

        .. code-block:: python

            from miniworldmaker import *

            board = Board()
            board.size = (100,60)
            Token(position=(10, 10))

            board.run()

        Output:

        .. image:: ../_images/token1.png
            :width: 100px
            :alt: Create a token

        Create a token with an image:

        .. code-block:: python

            from miniworldmaker import *

            board = Board(100,60)
            token = Token((10, 10))
            token.add_costume("images/player.png")

            board.run()

        Output:

        .. image:: ../_images/token2.png
            :width: 100px
            :alt: Create a Token with image

        .. code-block:: python

            import miniworldmaker

            class MyToken(miniworldmaker.Token):

                def on_setup(self):
                    self.add_costume("images/player.png")

            board = Board(100,60)
            my_token = MyToken(position = (40,130))
            board.run()

        Output:

        .. image:: ../_images/token1.png
            :width: 100px
            :alt: Create a token

        Create a Token at current mouse position:

        .. code-block:: python

            from miniworldmaker import *

            board = Board()

            @board.register
            def act(self):
                Token(self.get_mouse_position())

            board.run()

        .. image:: ../_images/token3.png
            :width: 100px
            :alt: Create a token at mouse position


    See Also:

        * See: :doc:`Token <../api/token>`
        * See: :doc:`Shapes <../api/token.shape>`
        * See: :doc:`TextTokens and NumberTokens <../api/token.texttoken>`
    """

    token_count: int = 0
    class_image: str = ""

    def __init__(self, position: Optional[Union[Tuple, "board_position.Position"]] = (0, 0), board=None):
        super().__init__(board)
        if position is None:
            self._position = (0, 0)
            position = (0, 0)
        else:
            self._position = position
        self._collision_type: str = "mask"
        self._dirty = 0
        self._layer: int = 0
        self._inner = 0
        self._size = (0, 0)
        self._static = False
        self.children = []
        # self._position: Union["board_position.Position", "board_position.PositionBase"] = position
        self.token_id: int = Token.token_count + 1
        self._board_sensor: "token_boardsensor.Boardsensor" = None
        self._position_manager: "token_position_manager.TokenPositionManager" = None
        self._costume_manager: "costumes_manager.CostumesManager" = None
        self._has_position_manager = False
        self._has_board_sensor = False
        self._has_costume_manager = False
        self._is_acting: bool = True  # is act method called?
        self._is_deleted = False
        try:
            self.board.get_token_connector(
                self).init_managers(position)
        except AttributeError:
            raise AttributeError("Token could not be created on a Board - Did you created a board instance before?")
        try:
            self._position = board_position.Position.create(position)
        except NoValidBoardPositionError:
            raise NoValidBoardPositionError(position)

        if not self.board:
            raise NoBoardError()
        pygame.sprite.DirtySprite.__init__(self)
        Token.token_count += 1
        self.speed: int = 1
        self.ask: "ask.Ask" = ask.Ask(self.board)
        self._dirty = 1

    @classmethod
    def create_on_board(cls, board):
        """Creates a token to a specific board

        overwritten in subclasses
        """
        return cls((0, 0), board)

    @property
    def collision_type(self) -> str:
        """collision_type specifies how collisions should be checked:

        * `default`: tile for TiledBoards, 'mask' for PixelBoards

        * `tile`: Are tokens on the same tile? (only TiledBoard)

        * `rect`: Are tokens colliding when checking their bounding - boxes? (Only PixelBoard)

        * `static-rect`: Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

        * `circle`: Are tokens colliding when checking circle with radius = bounding-box-radius.(Only PixelBoard)

        * `mask`: Are tokens colliding when checking if their image masks are overlapping.
        """
        if self._collision_type == "default":
            return "mask"
        else:
            return self._collision_type

    @property
    def sticky(self):
        return self._position_manager.sticky

    @sticky.setter
    def sticky(self, value):
        self._position_manager.sticky = value

    @collision_type.setter
    def collision_type(self, value: str):
        self._collision_type = value

    @property
    def layer(self) -> int:
        """defines layer the token is drawn, if multiple tokens overlap."""
        return self._layer

    @layer.setter
    def layer(self, value: int):
        self._layer = value
        self.board._tokens.change_layer(self, value)  # changes layer in DirtySpriteGroup.

    @property
    def last_position(self) -> "board_position.Position":
        """Token position in last frame

        Can be used to track changes.
        """
        return self.position_manager.last_position

    @property
    def last_direction(self) -> int:
        return self.position_manager.last_direction

    @classmethod
    def from_center(cls, center_position: "board_position.Position"):
        """
        Creates a token with center at center_position

        Args:
            center_position: Center of token
        """
        obj = cls(position=(0, 0))  # temp position
        obj.center = center_position  # pos set to center
        return obj

    @property
    def costume_count(self) -> int:
        """Returns number of costumes of token, 0 if token has no costume

        Examples:

            Add costume and count costumes

            .. code-block:: python

                from miniworldmaker import *
                board = Board()
                token = Token()
                assert token.costume_count == 0
                token.add_costume((255,0,0,0))
                assert token.costume_count == 1
                board.run()


        Returns:
            int: _description_
        """
        return self.costume_manager.length()

    @property
    def is_flipped(self) -> bool:
        """
        If a token is flipped, it is mirrored via the y-axis. You can use this property in 2d-plattformers
        to change the direction of token.

        .. note::

            It may be necessary to set ``is_rotatable = True``

        Examples:

            Flip a costume after 100 frames.

            .. code-block::

                from miniworldmaker import *

                board = Board(100,100)
                token = Token()
                token.add_costume("images/alien1.png")
                token.height= 400
                token.width = 100
                token.is_rotatable = False
                @token.register
                def act(self):
                    if self.board.frame % 100 == 0:
                        if self.is_flipped:
                            self.is_flipped = False
                        else:
                            self.is_flipped = True
                board.run()

            Output:

            .. raw:: html

                <video loop autoplay muted width=200>
                <source src="../_static/flipalien.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>

        Returns:
            True, if token is flipped

        """
        return self.costume.is_flipped

    @is_flipped.setter
    def is_flipped(self, value: bool):
        self.costume.is_flipped = value

    def flip_x(self) -> int:
        """Flips the actor by 180° degrees. The costume is flipped and the token's direction changed by 180 degrees.

        .. image:: ../_images/flip_x.png

        Examples:

            Flip a token in Example flipthefish.py

            .. code-block:: python

                from miniworldmaker import *

                board=TiledBoard()
                board.columns = 4
                board.rows = 1
                board.add_background("images/water.png")
                fish = Token()
                fish.border = 1
                fish.add_costume("images/fish.png")
                fish.direction = "right"
                fish.orientation = -90
                @fish.register
                def act(self):
                    self.move()

                @fish.register
                def on_not_detecting_board(self):
                    self.move_back()
                    self.flip_x()

                board.run()

            Output:

            .. raw:: html

                <video loop autoplay muted width=200>
                <source src="../_static/flipthefish.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>

        """
        return self.position_manager.flip_x()

    def add_costume(self, source: Union[None, Tuple, str, List] = None) -> "costume_mod.Costume":
        """Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            source: Path to the first image of new costume or Tuple with color-value

        Examples:

            Add first costume from image:

            .. code-block:: python

                from miniworldmaker import *

                board = Board((100,60))
                token = Token((10,10))
                costume = token.add_costume("images/player.png")

                board.run()


            Output:

            .. image:: ../_images/add_costume1.png
                :width: 100px
                :alt: Create Token with image as costume

            Add first costume from color:

            .. code-block:: python

                from miniworldmaker import *

                board = Board((100,60))
                token = Token((10,10))
                costume = token.add_costume((255,255,0))

                board.run()

            Output:

            .. image:: ../_images/add_costume2.png
                :width: 100px
                :alt: Create Token with image as costume


            Create two costumes and switch between costumes

            .. code-block:: python

                from miniworldmaker import *

                board = Board((100,60))
                token = Token((10,10))
                board.speed = 30
                costume1 = token.add_costume((255,255,0))
                costume2 = token.add_costume((255,0,255))
                @token.register
                def act(self):
                    if self.costume == costume1:
                        self.switch_costume(costume2)
                    else:
                        self.switch_costume(costume1)

                board.run()

            Output:

            .. image:: ../_images/add_costume3.png
                :width: 100%
                :alt: Create multiple costumes and switch between costumes

        Returns:
            The new costume.

        """

        if not source or type(source) in [str, tuple]:
            return self.costume_manager.add_new_appearance(source)
        elif type(source) == list:
            return cast("costume.Costume", self.costume_manager.add_new_appearance_from_list(source))
        else:
            raise MiniworldMakerError(f"Wrong type for appearance. Expected: list, tuple or str, got {type(source)}")

    def add_costumes(self, sources: list) -> "costume_mod.Costume":
        """Adds multiple costumes
        """
        return self.costume_manager.add_new_appearances(sources)

    def remove_costume(self, source: Union[int, "costume_mod.Costume"] = None):
        """Removes a costume from token

        Args:
            source: The index of the new costume or costume-object. Defaults to actual costume
        """
        if source is None:
            source = self.costume
        return self.costume_manager.remove_appearance(source)

    def switch_costume(self, source: Union[int, "appearance.Appearance"]) -> "costume_mod.Costume":
        """Switches the costume of token

        Args:
            source: Number of costume or Costume object

        Examples:

            Switch a costume:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(100,60)
                t = Token()
                costume =t1.add_costume("images/1.png")
                t.add_costume("images/2.png")
                t.switch_costume(1)

                @timer(frames = 40)
                def switch():
                    t1.switch_costume(0)

                board.run()

        Returns:
            The new costume
        """
        return self.costume_manager.switch_costume(source)

    def set_costume(self, costume: Union[str, tuple, int, "appearance.Appearance"]):
        if type(costume) == int or isinstance(costume, appearance.Appearance):
            self.switch_costume(costume)
        elif type(costume) in [str, tuple]:
            costume = self.add_costume(costume)
            self.switch_costume(costume)

    def reset_costumes(self):
        self.costume_manager.reset()

    def set_background_color(self, color: tuple):
        self.set_costume(color)

    def next_costume(self):
        """Switches to the next costume of token

        Returns:
            The new costume
        """
        self.costume_manager.next_costume()

    @property
    def costume(self) -> costume_mod.Costume:
        """Gets the costume of token
        """
        if hasattr(self, "costume_manager") and self.costume_manager is not None:
            return self.costume_manager.get_actual_appearance()

    @costume.setter
    def costume(self, value):
        self.costume_manager.appearance = value

    @property
    def costumes(self) -> "costumes_manager.CostumesManager":
        """Gets the costume manager
        
        The costume manager can be iterated to get all costumes
        """
        return self.costume_manager

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

        The default direction is ``0°``. All tokens are looking ``"up"``

        .. image:: /_images/movement.jpg
            :width: 100%
            :alt: Move on board

        **Values for Direction**

        * ``0°`` or ``"up"``: up
        * ``90°`` or ``"right"``: Move right
        * ``-90°`` or ``"left"``: Move left
        * ``180°`` or ``"down"``: Move down
        * ``"forward"``: Current direction

        Sets direction of the token.

        You can use an integer or a string to describe the direction

        Options
            * ``0``, ``"up"`` - Look up
            * ``90``, ``"right"``, - Look right
            * ``-90``, ``"left"``, - Look left
            * ``-180``, ``180``, ``"down"`` - Look down

        .. image:: ../_images/direction.png

        Examples:

            Move in a direction with WASD-Keys

            .. code-block:: python

                def on_key_down(self, keys):
                    if "W" in keys:
                        self.direction = "up"
                    elif "S" in keys:
                        self.direction = "down"
                    elif "A" in keys:
                        self.direction = "left"
                    elif "D" in keys:
                        self.direction = "right"
                    self.move()

            Move 45°:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(100, 100)
                c = Circle ((50,50), 10)

                @c.register
                def act(self):
                    c.direction = 45
                    c.move()
                        
                board.run()


            .. raw:: html

                <video loop autoplay muted width=400>
                <source src="../_static/move45.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>

            Move -45°:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(100, 100)
                c = Circle ((50,50), 10)

                @c.register
                def act(self):
                    c.direction = -45
                    c.move()
                        
                board.run()

            .. raw:: html

                <video loop autoplay muted width=400>
                <source src="../_static/moveminus45.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>
        """
        return self.position_manager.direction

    @direction.setter
    def direction(self, value: int):
        self.position_manager.direction = value

    @property
    def direction_at_unit_circle(self) -> int:
        """Gets the direction as value in unit circle (0° right, 90° top, 180° left...)
        """
        return self.position_manager.dir_to_unit_circle(self.direction)

    @direction_at_unit_circle.setter
    def direction_at_unit_circle(self, value: int):
        """Sets the direction from unit circle
        Args:
            value: An angle in the unit circle, e.g. 0°: right, 90° top, ...
        """
        self.direction = self.position_manager.unit_circle_to_dir(value)

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        .. image:: ../_images/turn_left.png

        Options:
          * You can set the value token.is_rotatable = False if you don't want the token to be rotated.

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(100, 100)
                t = Token()
                t.add_costume("images/arrow.png")
                t.size = (100,100)

                @t.register
                def act(self):
                    t.turn_left(1)
                    
                board.run()

            Output:

            .. raw:: html
       
                <video loop autoplay muted width=400>
                <source src="../_static/turnleft.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        return self.position_manager.turn_left(degrees)

    def turn_right(self, degrees: Union[int, float] = 90):
        """Turns token by *degrees* degrees right

        .. image:: ../_images/turn_right.png

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(100, 100)
                t = Token()
                t.add_costume("images/arrow.png")
                t.size = (100,100)

                @t.register
                def act(self):
                    t.turn_left(1)
                    
                board.run()

        Output:
       
        .. raw:: html
        
            <video loop autoplay muted width=400>
            <source src="../_static/turnright.webm" type="video/webm">
            Your browser does not support the video tag.
            </video>

        Options:
          * You can set the value token.is_rotatable = False if you don't want the token to be rotated.

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        return self.position_manager.turn_right(degrees)

    def point_in_direction(self, direction: Union[str, int, float]) -> "board_direction.Direction":
        """Token points in given direction.

        You can use a integer or a string to describe the direction

        Args:
            The direction as integer or string (see options)

        Options
            * ``0``, ``"up"`` - Look up
            * ``90``, ``"right"``, - Look right
            * ``-90``, ``"left"``, - Look left
            * ``-180``, ``180``, ``"down"`` - Look down

        .. image:: ../_images/direction.png

        Examples:

            Move in a direction with WASD-Keys

            .. code-block:: python

              def on_key_down(self, keys):
                  if "W" in keys:
                      self.direction = "up"
                  elif "S" in keys:
                      self.direction = "down"
                  elif "A" in keys:
                      self.direction = "left"
                  elif "D" in keys:
                      self.direction = "right"
                  self.move()
        """
        return self.position_manager.point_in_direction(direction)

    def point_towards_position(self, destination: Union[tuple, "board_position.BoardPosition"]) -> Union[int, float]:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        Examples:

            Point towards mouse_position:

            .. code-block:: python

                def act(self):
                    mouse = self.board.get_mouse_position()
                if mouse:
                    self.point_towards_position(mouse)
                self.move()
        """
        return self.position_manager.point_towards_position(destination)

    def point_towards_token(self, other: "Token") -> int:
        """Token points towards another token.

        Args:
            other: The other token

        Returns:
            The new direction

        """
        pos = other.get_global_rect().center
        return self.point_towards_position(pos)

    @property
    def size(self) -> tuple:
        """Size of the token"""
        return self.position_manager.size

    @size.setter
    def size(self, value: tuple):
        self.set_size(value)

    def set_size(self, value: tuple):
        self.position_manager.set_size(value)

    @property
    def width(self):
        """The width of the token in pixels.

        When the width of a token is changed, the height is scaled proportionally.

        Examples:

            Create a token and scale width/height proportionally:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                def create_token(x, y):
                t = Token()
                t.position = (x, y)
                t.add_costume("images/alien1.png")
                t.border = 1
                return t

                t0 = create_token(0,0)
                t1 = create_token(50,0)
                t1.height = 400
                t2 = create_token(300,0)
                t2.width = 180

                board.run()

            .. image:: ../_images/widthheight.png
                :alt: Textured image
        """
        return self.position_manager.get_size()[0]

    @width.setter
    def width(self, value):
        self.position_manager.set_width(value)
        self.on_shape_change()

    def scale_width(self, value):
        old_width = self.size[0]
        old_height = self.size[1]
        scale_factor = value / old_width
        self.size = (value, old_height * scale_factor)

    @property
    def height(self):
        """The height of the token in pixels.

        When the height of a token is changed, the width is scaled proportionally.

        Examples:

            Create a token and scale width/height proportionally:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                def create_token(x, y):
                t = Token()
                t.position = (x, y)
                t.add_costume("images/alien1.png")
                t.border = 1
                return t

                t0 = create_token(0,0)
                t1 = create_token(50,0)
                t1.height = 400
                t2 = create_token(300,0)
                t2.width = 180

                board.run()

            .. image:: ../_images/widthheight.png
                :alt: Textured image
        """
        return self.position_manager.get_size()[1]

    @height.setter
    def height(self, value):
        self.position_manager.set_height(value)
        self.on_shape_change()

    def scale_height(self, value):
        old_width = self.size[0]
        old_height = self.size[1]
        scale_factor = value / old_height
        self.size = (old_width * scale_factor, value)

    @property
    def x(self) -> float:
        """The x-value of a token"""
        return self.position_manager.get_position()[0]

    @x.setter
    def x(self, value: float):
        self.set_position((value, self.y))

    @property
    def y(self) -> float:
        """The y-value of a token"""
        return self.position_manager.get_position()[1]

    @y.setter
    def y(self, value: float):
        self.set_position((self.x, value))

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
        return self.get_global_rect().topleft[0]

    @property
    def topleft_y(self):
        """x-value of token topleft-position"""
        return self.get_global_rect().topleft[1]

    @property
    def topleft(self) -> "board_position.Position":
        return self.position_manager.topleft

    @topleft.setter
    def topleft(self, value: Union[Tuple, "board_position.Position"]):
        self.position_manager.topleft = value

    @property
    def center_y(self):
        """y-value of token center-position"""
        return self.position_manager.center_y

    @property
    def center(self) -> "board_position.Position":
        return self.position_manager.center

    @property
    def local_center(self):
        """x-value of token center-position"""
        return self.position_manager.local_center

    @center_x.setter
    def center_x(self, value: float):
        self.position_manager.center_x = value

    @center_y.setter
    def center_y(self, value: float):
        self.position_manager.center_y = value

    @center.setter
    def center(self, value: Union[Tuple, "board_position.Position"]):
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

            if token is on the board, move forward:

            .. code-block:: python

                class Robot(Token):

                    def act(self):
                        if self.detecting_board():
                            self.move()
        """
        return self.position_manager.move(distance)

    def move_vector(self, vector):
        """Moves actor in direction defined by the vector

        Returns:
            The moved token

        """
        return self.position_manager.move_vector(vector)

    def move_up(self, distance: int = 1):
        return self.position_manager.move_in_direction("up", distance)

    def move_down(self, distance: int = 1):
        return self.position_manager.move_in_direction("down", distance)

    def move_left(self, distance: int = 1):
        return self.position_manager.move_in_direction("left", distance)

    def move_right(self, distance: int = 1):
        return self.position_manager.move_in_direction("right", distance)

    def move_back(self):
        """deprecated - use: undo_move()

        In next versions, this functions will move the token backwards
        """
        return self.position_manager.undo_move()

    def undo_move(self):
        """Undo the last move. Moves the actor to the last position and resets direction.

        .. image:: ../_images/move_back.png

        Returns:
            The moved token

        Examples:

            move_back when field is blocked:

            .. code-block:: python

                def on_sensing_wall(self, wall):
                    self.undo_move()

        """
        return self.position_manager.undo_move()

    def move_towards(self, position):
        return self.position_manager.move_towards_position(position)

    def move_in_direction(self,
                          direction: Union[int, str, tuple, "board_direction.Direction", "board_position.Position"],
                          distance=1):
        """Moves token *distance* steps into a *direction* or towards a position

        .. image:: ../_images/move_in_direction.png

        Options
            * 0, "up" - Look up
            * 90, "right", - Look right
            * -90, "left", - Look left
            * -180, 180, "down" - Look down

        .. image:: ../_images/direction.png

        Args:
            direction: Direction as angle
            distance: Senses obj "distance" steps in front of current token.

        Returns:
            The token itself

        """
        if type(direction) in [int, str, board_direction.Direction]:
            return self.position_manager.move_in_direction(direction, distance)
        elif type(direction) == tuple or isinstance(direction, board_position.Position):
            return self.position_manager.move_towards_position(direction, distance)
        else:
            raise MiniworldMakerError(f"Expected direction or position, got f{type(direction)}, ({direction})")

    def move_to(self, position: "board_position.Position"):
        """Moves token *distance* to a specific board_posiition

        Args:
            position: The position to which the actor should move. The position can be a 2-tuple (x, y)
            which will be converted to a board_position

        .. image:: ../_images/move_to.png

        Returns:
            The token itself

        Examples:

            move to (3, 2) on mouse_click

            .. code-block:: python

                def on_clicked_left(self, position):
                    self.move_to((3,2))


        """
        return self.position_manager.move_to(position)

    def remove(self, kill=True):
        """
        Removes this token from board

        Examples:

            Removes robots in thecrash.py :

            .. code-block:: python

               def act(self):
                   self.move()
                   other = self.sensing_token(distance = 0, token_type=Robot)
               if other:
                   explosion = Explosion(position=self.position)
                   self.remove()
                   other.remove()
        """
        if kill is True:
            if hasattr(self, "board") and self.board:
                self.board.get_token_connector(self).delete_token()
        else:
            if hasattr(self, "board") and self.board:
                self.board.get_token_connector(self).remove_token_from_board()

    @property
    def is_rotatable(self) -> bool:
        """Defines if the costume of a token should be rotatable. The token can still be rotated with
        the ``direction`` property, but its costume won't be changed

        .. note::

            You can also use ``token.costume.is_rotatable``

        Examples:

            Create a rotatable and a not rotatable token

            .. code-block::

                from miniworldmaker import *
                board = Board()

                t1 = Token((100,100))
                t1.add_costume("images/alien1.png")

                t2 = Token((200,200))
                t2.add_costume("images/alien1.png")
                t2.is_rotatable = False

                @t1.register
                def act(self):
                    self.move()
                    self.direction += 1

                @t2.register
                def act(self):
                    self.move()
                    self.direction += 1

                board.run()


            Output:

            .. raw:: html

                <video loop autoplay muted width=400>
                <source src="../_static/rotatable.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>

        """
        return self.costume.is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value: bool):
        self.costume.is_rotatable = value

    def bounce_from_border(self, borders: List[str]) -> Token:
        """The actor "bounces" from a border.

        The direction is set according to the principle input angle = output angle.

        .. note::

          You must check for borders first!

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Examples:

            .. code-block:: python

                from miniworldmaker import *
                import random

                board = Board(150, 150)
                token = Token((50,50))
                token.add_costume("images/ball.png")
                token.direction = 10

                @token.register
                def act(self):
                    self.move()
                    borders = self.sensing_borders()
                    if borders:
                        self.bounce_from_border(borders)

                board.run()

            Output:

            .. raw:: html

                <video loop autoplay muted width=240>
                <source src="../_static/bouncing_ball.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>


        Returns:
            The token

        """
        return self.position_manager.bounce_from_border(borders)

    def on_not_detecting_board(self):
        """`on_not_detecting_board` is called, when token is not on the board.

        Examples:

            Register on_not_detecting_board method:

            .. code-block::

                @player.register
                    def on_not_detecting_board(self):
                    print("Warning: I'm not on the board!!!")

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_not_detecting_board())

    def detect_all(self, token_filter: str = None, direction: int = 0, distance: int = 0) -> List["Token"]:
        """Detects if tokens are on token position.
        Returns a list of tokens.

        .. image:: ../_images/sensing_tokens.png

        Args:
            token_filter: filter by token type. Enter a class_name of tokens to look for here
            direction: The direction in which tokens should be detected.
            distance:  The distance in which tokens should be detected (Start-Point is token.center)

        Returns:
            All tokens found by Sensor

        """
        if distance == 0:
            return self.board_sensor.detect_tokens(token_filter)
        else:
            return self.board_sensor.detect_tokens_at(token_filter, direction, distance)

    detect_tokens = detect_all  #: Alias of :meth:`Token.detect_all`
    sensing_tokens = detect_tokens  #: Alias of :meth:`Token.sensing_tokens`

    def detect(self, token_filter: Union[str, type] = None, direction: int = 0, distance: int = 0) -> Union[
        "Token", None]:
        """Senses if tokens are on token position.
        Returns the first found token.

        .. image:: ../_images/sensing_token.png

        Args:
            token_filter: filter by token type. Enter a class_name of tokens to look for heredirection: int = 0, distance: int = 0
            direction: The direction in which tokens should be detected.
            distance:  The distance in which tokens should be detected (Start-Point is token.center)

        Returns:

            First token found by Sensor

        Examples:

            The green robot pushes the yellow robot:

            .. code-block:: python

                from miniworldmaker import *

                board = TiledBoard(8,3)
                token = Token((1,1))
                token.add_costume("images/robo_green.png")
                token.orientation = -90
                token.direction = 90

                token2 = Token((4,1))
                token2.add_costume("images/robo_yellow.png")
                token2.orientation = -90
                token2.direction = -90

                @token.register
                def act(self):
                    self.move()
                    token = self.sensing_token()
                    if token:
                        token.move_right()
                board.run()

            Output:

            .. raw:: html

                <video loop autoplay muted width=240>
                <source src="../_static/pushing.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>
        """
        if distance == 0:
            return self.board_sensor.detect_token(token_filter)
        else:
            return self.board_sensor.detect_tokens_at(token_filter, direction, distance)

    detect_token = detect
    sensing_token = detect  #: Alias of :meth:`Token.detect`

    def detect_borders(self, distance: int = 0, ) -> List:
        """
        Senses borders

        .. image:: ../_images/sensing_borders.png

        Args:

            distance: Specifies the distance in front of the actuator to which the sensors reacts.

        Returns:

            True if border was found.

        """
        return self.board_sensor.detect_borders(distance)

    sensing_borders = detect_borders  #: Alias of :meth:`Token.sensing_borders`

    def detect_left_border(self) -> bool:
        """Does the token touch the left border?

        Returns:
            True if border was found.

        """
        return "left" in self.board_sensor.detect_borders(0)

    sensing_left_border = detect_left_border
    is_sensing_left_border = sensing_left_border  #: Alias of :meth:`Token.sensing_left_border`

    def detect_right_border(self) -> bool:
        """Does the token touch the right border?

        Returns:
            True if border was found.

        """
        return "right" in self.board_sensor.detect_borders(0)

    sensing_right_border = detect_right_border
    is_sensing_right_border = sensing_right_border  #: Alias of :meth:`Token.sensing_right_border`

    def detect_top_border(self) -> bool:
        """Does the token touch the lower border?

        Returns:
            True if border was found.

        """
        return "top" in self.board_sensor.detect_borders(0)

    sensing_top_border = detect_top_border
    is_sensing_top_border = sensing_top_border  #: Alias of :meth:`Token.sensing_top_border`

    def sensing_bottom_border(self) -> bool:
        """Does the token touch the lower border?

        Returns:
            True if border was found.

        """
        return "bottom" in self.board_sensor.detect_borders(0)

    is_sensing_bottom_border = sensing_bottom_border  #: Alias of :meth:`Token.sensing_bottom_border`
    is_touching_bottom_border = sensing_bottom_border  #: Alias of :meth:`Token.sensing_bottom_border`

    def detect_color(self, color: Tuple = None) -> bool:
        """Senses colors in board-background at token center-position

        Args:
            color: color as tuple
            
        Returns:
            True, if color was found

        """
        color = self.board_sensor.detect_color(color, )
        return color

    sensing_color = detect_color

    def detect_colosr(self, color: List = None) -> bool:
        """Senses colors in board-background at token center-position

        Args:
            color: A list of colors

        Returns:
            True, if any color was found

        """
        color = self.board_sensor.detect_colors(color, )
        return color

    def detect_color_at(self, direction: int = None, distance: int = 0) -> Union[Tuple, List]:
        """Detects colors in board-background at token-position

        Args:
            direction: Specifies the direction where the sensors is searching.
            distance: Specifies the distance in front of the actuator to which the sensors reacts.

        Returns:
            All colors found by Sensor

        """
        color = self.board_sensor.detect_color_at(direction, distance)
        return color

    sensing_color_at = detect_color_at
    sense_color_at = detect_color_at

    def detect_tokens_at(self, direction=None, distance=0, token_filter=None) -> list:
        """Detects a token in given direction and distance.

        Examples:

          .. code-block:: python

            from miniworldmaker import *
            board = Board()
            wall=Rectangle((200,0))
            wall.size = (20, 400)

            for i in range(7):
                token = Circle((10,i*60 + 20))
                token.range = i * 10
                @token.register
                def act(self):
                    if not self.detect_tokens_at(self.direction, self.range):
                        self.direction = "right"
                        self.move()

            board.run()


        :param direction: The direction in which tokens should be detected.
        :param distance:  The distance in which tokens should be detected (Start-Point is token.center)
        :return: A list of tokens
        """
        return self.board_sensor.detect_tokens_at(token_filter, direction, distance)

    sensing_tokens_at = detect_tokens  #: Alias of :meth:`Token.sensing_tokens_at`

    def detect_token_at(self, direction=None, distance=0, token_filter=None) -> "Token":
        found_tokens = self.board_sensor.detect_tokens_at(token_filter, direction, distance)
        if found_tokens:
            return found_tokens[0]

    def detect_tokens_in_front(self, token_filter=None, distance=1, ) -> list:
        return self.board_sensor.detect_tokens_at(token_filter, self.direction, distance)

    def detect_token_in_front(self, token_filter=None, distance=1, ) -> "Token":
        found_tokens = self.board_sensor.detect_tokens_at(token_filter, self.direction, distance)
        if found_tokens:
            return found_tokens[0]

    def detect_point(self, position: Union["board_position.Position", Tuple]) -> bool:
        """Is the token colliding with a specific (global) point?

        Returns:
            True if point is below token
        """
        return self.board_sensor.detect_point(position)

    sensing_point = detect_point

    def detect_rect(self, rect: Union[Tuple, pygame.rect.Rect]):
        """Is the token colliding with a static rect?"""
        return self.board_sensor.detect_rect(rect)

    is_touching_rect = detect_rect

    def bounce_from_token(self, other: "Token"):
        self.position_manager.bounce_from_token(other)

    def animate(self, speed: int = 10):
        self.costume_manager.animate(speed)

    def animate_costume(self, costume: "costume_mod.Costume", speed: int = 10):
        self.costume_manager.animate_costume(costume, speed)

    def animate_loop(self, speed: int = 10):
        """Animates a costume with a looping animation

        Switches through all costume-images every ``speed``-frame.

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(columns=280, rows=100)
                robo = Token(position=(0, 0))
                robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
                robo.size = (99, 99)
                robo.animate_loop()
                board.run()

        Args:
            speed (int, optional): Every ``speed`` frame, the image is switched. Defaults to 10.
        """
        self.costume.loop = True
        self.costume_manager.animate(speed)

    def stop_animation(self):
        """Stops current animation. 
        Costume ``is_animated`` is set to False


        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(columns=280, rows=100)
                robo = Token(position=(0, 0))
                robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
                robo.size = (99, 99)
                robo.animate_loop()
                @timer(frames = 100)
                def stop():
                    robo.stop_animation()
                board.run()
        """
        self.costume.is_animated = False

    def send_message(self, message: str):
        """Sends a message to board.

        The message can be received with the ``on_message``-event

        Examples:

            Send and receive messages:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()

                token1 = Token((2, 2))
                token1.add_costume((100,0,100,100))

                @token1.register
                def on_message(self, message):
                    print("Received message:" + message)

                token2 = Token((100,100))
                token2.send_message("Hello from token2")

                @token2.register
                def on_key_down_s(self):
                    self.send_message("Hello")
                board.run()

        Args:
            message (str): A string containing the message.
        """
        self.board.app.event_manager.to_event_queue("message", message)

    def on_key_down(self, key: list):
        """**on_key_down**  is called one time when a key is pressed down.

        .. note::
            Instead of **on_key_down** you can use **on_key_down_letter**, e.g. **on_key_down_a** or **on_key_down_w**
            , if you want to handle an on_key_down event for a specific letter.

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
        raise NotImplementedOrRegisteredError(self.on_key_down)

    def on_key_pressed(self, key: list):
        """**on_key_pressed** is called when while key is pressed. If you hold the key, on_key_pressed
        is repeatedly called again and again until the key is released.

        .. note::

            Like `on_key_down` the method can be called in the variant `on_key_pressed_[letter]`
            (e.g. `on_key_pressed_w(self)`).

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
            key (list): The typed key as list (e.g. ['C', 'c', 'D', 'd']) containing both uppercase and lowercase
            of typed letter.

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_key_pressed)

    def on_key_up(self, key):
        raise NotImplementedOrRegisteredError(self.on_key_up)

    def on_mouse_over(self, position):
        """on_mouse_over is called, when mouse is moved over token
        :param position: The mouse position
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_over)

    def on_mouse_leave(self, position):
        """on_mouse_over is called, when mouse is moved over token
        :param position: The mouse position
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_over)

    def on_mouse_left(self, position: tuple):
        """on_mouse_left is called when left mouse button was pressed.
        You must *register* or *implement* this method as an event.

        .. note::

            The event is triggered, when mouse-left was clicked, even when the current mouse position
            is not related to token position.

            You can use :py:meth:`Token.sensing_point` to check, if the mouse_position is *inside* the token.

        Examples:

            A circle will be moved, if you click on circle.

            .. code-block::

                from miniworldmaker import *

                board = Board(120,40)
                circle = Circle((20, 20))
                circle.direction = 90

                @circle.register
                def on_mouse_left(self, mouse_pos):
                    if self.sensing_point(mouse_pos):
                        self.move()

                board.run()

        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """

        raise NotImplementedOrRegisteredError(self.on_mouse_left)

    def on_mouse_right(self, position: tuple):
        """Method is called when right mouse button was pressed.
        You must *register* or *implement* this method as an event.

        .. note::

            The event is triggered, when mouse was clicked,even when the current mouse position is not related
            to token position.

            You can use :py:meth:`Token.sensing_point` to check, if the mouse_position is *inside* the token.

        Examples:

            See: :py:meth:`Token.on_mouse_left`.
        
        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_right)

    def on_mouse_motion(self, position: tuple):
        """Method is called when mouse moves. You must *register* or *implement* this method as an event.

        .. note::

            The event is triggered, when mouse is moved, even when the current mouse position
            is not related to token position.

            You can use :py:meth:`Token.sensing_point` to check, if the mouse_position is *inside* the token.

        Examples:

            A circle will be moved, if you click on circle.

            .. code-block::

                from miniworldmaker import *

                board = Board(120,40)
                circle = Circle((20, 20))
                circle.direction = 90

                @circle.register
                def on_mouse_motion(self, mouse_pos):
                    if self.sensing_point(mouse_pos):
                        self.move()

                board.run()

        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_motion)

    def on_mouse_left_released(self, position: tuple):
        """Method is called when left mouse key is released. 

        Examples:

            You can use on_mouse_left_release to implement a drag_and_drop event

            .. code-block::

                from miniworldmaker import *

                board = Board(200, 200)
                circle = Circle((30, 30), 60)
                circle.direction = 90
                circle.dragged = False

                @circle.register
                def on_mouse_left(self, mouse_pos):
                    if self.sensing_point(mouse_pos):
                        self.dragged = True
                        
                @circle.register
                def on_mouse_left_released(self, mouse_pos):
                    if not board.is_mouse_pressed():
                        self.dragged = False
                        self.center = mouse_pos
                        
                board.run()

            Output:

            .. raw:: html

                <video loop autoplay muted width=200>
                <source src="../_static/draganddrop.webm" type="video/webm">
                Your browser does not support the video tag.
                </video>


        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_left_released)

    def on_mouse_right_released(self, position: tuple):
        """Method is called when right mouse key is released. See :py:meth:`Token.on_mouse_left_released`.


        Args:
            position (tuple): Actual mouse position as tuple (x,y)

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_mouse_right_released)

    def on_message(self, message: str):
        """Messages are used to allow objects to communicate with each other.

        Send a message:

        * A token and the board can send a message to all tokens and the board with the command:
          `self.send_message(“message_string”)`

        Process a message:

        * If your board or your token should react to messages you can use the event on_message:

        Examples:

            Receive a message:

            .. code-block:: python

                @player.register
                def on_message(self, message):
                    if message == "Example message":
                    do_something()

        Args:
            message (str): The message as string

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError(self.on_message)

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
        raise NotImplementedOrRegisteredError(self.on_clicked_left)

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
        raise NotImplementedOrRegisteredError(self.on_clicked_right)

    def on_detecting_board(self):
        """`on_detecting_board` is called, when token is on the board

        Examples:

            Register on_detecting_board method:

            .. code-block::

                @player.register
                    def on_detecting_board(self):
                    print("Player 3: I'm on the board:")

        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.

        """
        raise NotImplementedOrRegisteredError(self.on_detecting_board)

    @property
    def static(self):
        """Should token react to events?
        You can turn this option off for additional performance boost.
        """
        return self._static

    @static.setter
    def static(self, value):
        _token_connector = self.board.get_token_connector(self)
        _token_connector.set_static(value)

    @property
    def fill_color(self):
        """The fill color of token as rgba value, e.g. (255, 0, 0) for red.
        
        When ``fill_color`` is set to a color, the attribute ``is_filled`` of costume
        (See: :py:attr:.appearances.appearance.Appearance.is_filled`) is set to ``True``.
        
        .. note::

            Aliases: :py:attr:`Token.color`

        .. warning:: 
        
            If you fill a costume with an image, the image will be completely overwritten,
            even if `fill_color` is transparent.
        
            This behaviour may change in later releases!

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(200,80)
                board.default_fill_color = (0,0, 255)

                t = Token()

                t2 = Token((40,0))
                t2.is_filled = (0, 255, 0)

                t3 = Token((80, 0))
                t3.fill_colorimport miniworldmaker.tokens.token as token
 = (255, 0, 0)

                t4 = Token((120, 0))
                t4.add_costume((0,0,0))
                t4.fill_color = (255, 255, 0)

                t5 = Token((160, 0))
                t5.add_costume("images/player.png")
                t5.fill_color = (255, 255, 0, 100) # image is overwritten

                t6 = Circle((0, 40), 20)
                t6.position = t6.center
                t6.fill_color = (255, 255, 255)

                t7 = Ellipse((40, 40), 40, 40)
                t7.fill_color = (255, 0, 255) 

                board.run()

            Output:

            .. image:: ../_images/fill_color.png
                :width: 200px
                :alt: Set borders
        """
        return self.costume.fill_color

    @fill_color.setter
    def fill_color(self, value):
        self.costume.fill(value)

    # Alias
    color = fill_color

    def fill(self, value):
        """Set fill color for borders and lines"""
        self.costume.fill(value)

    @property
    def is_filled(self):
        """Is token filled with color?"""
        return self.costume.is_filled

    @is_filled.setter
    def is_filled(self, value):
        self.costume.fill(value)

    @property
    def border_color(self):
        """border color of token.

        The border-color is a rgba value, for example (255, 0, 0) for red, (0, 255, 0) for green and (255, 0, 0, 100).

        If the color-value has 4 values, the last value defines the transparency:
          * 0: Full transparent,
          * 255: No transparency


        .. note:: 

            You must also set :py:attr:`Token.border` to a value > 0

            Aliases:  :py:attr:`Token.stroke_color`

        Examples:

            See :py:attr:`Token.border`


        """
        return self.costume.border_color

    @border_color.setter
    def border_color(self, value):
        self.costume.border_color = value

    # Alias

    stroke_color = border_color

    @property
    def border(self):
        """The border-size of token.

        The value is 0, if token has no border.

        .. note::

            You can also set border with ``costume.border`` or you can set the border with ``board.default_border``

        Examples:

            Set border of token:

            .. code-block::

                from miniworldmaker import *

                board = Board(210,80)
                board.default_border_color = (0,0, 255)
                board.default_border = 1

                t = Token((10,10)) # default-border and color from bord
                t.add_costume("images/player.png")

                t2 = Token ((60, 10)) # overwrites default border values
                t2.add_costume("images/player.png")
                t2.border_color = (0,255, 0)
                t2.border = 5

                t3 = Token ((110, 10)) # removes border
                t3.add_costume("images/player.png")
                t3.border = None

                board.run()

            Output:

            .. image:: ../_images/borders.png
                :width: 200px
                :alt: Set borders
        """
        return self.costume.border

    @border.setter
    def border(self, value):
        self.costume.border = value

    def hide(self):
        """Hides a token (the token will be invisible)
        """
        self.visible = False

    def show(self):
        """Displays a token ( an invisible token will be visible)
        """
        self.visible = True

    def register(self, method: callable, force=False, name=None):
        """This method is used for the @register decorator. It adds a method to an object

        Args:
            method (callable): The method which should be added to the token
            force: Should register forced, even if method is not handling a valid event?
            name: Registers method with specific name
        """
        if not force and method.__name__ not in self.board.event_manager.token_class_events_set:
            raise RegisterError(method.__name__, self)
        bound_method = token_inspection.TokenInspection(self).bind_method(method, name)
        if method.__name__ == "on_setup":
            self.on_setup()
        self.board.event_manager.register_event(method.__name__, self)
        return bound_method

    def get_local_rect(self) -> pygame.Rect:
        local_rect = self.position_manager.get_local_rect()
        return local_rect

    def get_global_rect(self) -> pygame.Rect:
        if self.position_manager:
            return self.position_manager.get_global_rect()
        return pygame.Rect(-1, -1, 0, 0)

    @property
    def rect(self) -> pygame.Rect:
        """The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.
        """
        local_rect = self.position_manager.get_local_rect()
        # local_rect.topleft = self.board.container_top_left_x + local_rect.topleft[0], self.board.container_top_left_y + \
        #                     local_rect.topleft[1]
        return local_rect

    def get_rect(self) -> pygame.Rect:
        """Gets the rect of the token.
        
        If a camera is used, the local rect is written.

        Returns:
            pygame.Rect: A Rectangle with local position.
        """
        return self.position_manager.get_local_rect()

    def __str__(self):
        if self.board and hasattr(self, "position_manager") and self.position_manager:
            return "**Token: ID: {1} at pos {2} with size {3}**".format(
                self.__class__.__name__, self.token_id, self.position, self.size
            )
        else:
            return "**Token: {0} ; ID: {1}**".format(self.__class__.__name__, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        """
        The image of the token:

        .. warning::
          Warning: You should not directly draw on the image
          as the image will be reloaded during animations

        """
        return self.costume_manager.image

    @property
    def position_manager(self):
        # if not hasattr(self, "_position_manager") or not self._position_manager:
        #    return None
        try:
            return self._position_manager
        except:
            MissingPositionManager()

    @property
    def board_sensor(self):
        try:
            return self._board_sensor
        except AttributeError:
            raise MissingBoardSensor()

    @property
    def costume_manager(self):
        return self._costume_manager

    @property
    def position(self) -> "board_position.Position":
        """The position of the token as Position(x, y)
        """
        return self.position_manager.position

    @position.setter
    def position(self, value: Union["board_position.Position", tuple]):
        self.set_position(value)

    def set_position(self, value: Union["board_position.Position", tuple]):
        self.position_manager.position = value

    def get_distance_to(self, obj: Union["Token", "board_position.Position", tuple]) -> float:
        """Gets the distance to another token or a position

        Args:
            obj: Token or Position

        Returns:
            float: The distance between token (measured from token.center) to token or position.
        """
        return self.board_sensor.get_distance_to(obj)

    def on_shape_change(self):
        pass
