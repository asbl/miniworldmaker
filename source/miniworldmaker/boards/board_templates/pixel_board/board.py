import math
from typing import Tuple, Union, Type, Optional, List, cast

import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.background as background_mod
import miniworldmaker.appearances.backgrounds_manager as backgrounds_manager
import miniworldmaker.base.app as app
import miniworldmaker.boards.board_base as board_base
import miniworldmaker.boards.board_manager.board_collision_manager as coll_manager
import miniworldmaker.boards.board_manager.board_event_manager as event_manager
import miniworldmaker.boards.board_manager.board_mouse_manager as mouse_manager
import miniworldmaker.boards.board_manager.board_music_manager as board_music_manager
import miniworldmaker.boards.board_manager.board_sound_manager as board_sound_manager
import miniworldmaker.dialogs.ask as ask
import miniworldmaker.positions.direction as board_direction
import miniworldmaker.positions.position as board_position
import miniworldmaker.positions.rect as board_rect
import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tools.board_inspection as board_inspection
import miniworldmaker.tools.color as color
import miniworldmaker.tools.timer as timer
import pygame
from miniworldmaker.exceptions.miniworldmaker_exception import (
    BoardArgumentsError,
)


class Board(board_base.BaseBoard):
    """A board is a playing field on which tokens can move.

    A board has a `background` and provides basic functions for the positioning of
    tokens and for the collision detection of tokens, which can be queried via the sensors of the tokens.

    You can create your own board by creating a class that inherits from Board or you can directly create a board
    object of type `Board` or one of its child classes (`TiledBoard`, `PhysicsBoard`, ...).

    *Board*

    A board for pixel accurate games.

    * The position of a token on a Board is the pixel at topleft of token.

    * New tokens are created with top-left corner of token rect at position.

    * Two tokens collide when their sprites overlap.

    .. image:: ../_images/asteroids.jpg
        :alt: Asteroids

    **Other Boards:**

    * TiledBoard: For Boards using Tiles, like rogue-like rpgs, see
      :doc:`TiledBoard <../api/board.tiledboard>`)
    * PhysicsBoard: For Boards using the PhysicsEngine, see
      :doc:`PhysicsBoard <../api/board_physicsboard>`)

    Examples:

        Creating a TiledBoard Object:

        .. code-block:: python

            from miniworldmaker import *

            my_board = TiledBoard()
            my_board.columns = 30
            my_board.rows = 20
            my_board.tile_size = 20


        Creating a TiledBoard-Subclass.

        .. code-block:: python

            import miniworldmaker

            class MyBoard(miniworldmaker.TiledBoard):

                def on_setup(self):
                    self.columns = 30
                    self.rows = 20
                    self.tile_size = 20

        Creating a Board Object:

        .. code-block:: python

            from miniworldmaker import *

            my_board = Board()
            my_board.columns = 300
            my_board.rows = 200

        Creating a Board Subclass

        .. code-block:: python

            import miniworldmaker

            class MyBoard(miniworldmaker.Board):

                def on_setup(self):
                    self.columns = 300
                    self.rows = 200


    See also:

        * See: :doc:`Board <../api/board>`
        * See: :doc:`TiledBoard <../api/board.tiledboard>`


    Args:
        view_x: columns of new board (default: 40)
        view_y: rows of new board (default:40)
        tile_size: Size of tiles (1 for normal Boards, can differ for TiledBoards)
    """

    def __init__(
            self,
            view_x: Union[int, Tuple[int]] = 400,
            view_y: int = 400,
            tile_size: int = 1,
    ):
        if type(view_x) != int or type(view_y) != int:
            # If first param is tuple, generate board from tuple-data
            if type(view_x) == tuple:
                size = view_x
                view_x = size[0]
                view_y = size[1]
            else:
                raise BoardArgumentsError(view_x, view_y)
        self._tile_size = tile_size
        self.camera = self._get_camera_manager_class()(view_x, view_y, self)
        self._tokens = pygame.sprite.LayeredDirty()
        self.event_manager: event_manager.BoardEventManager = self._create_event_manager()
        super().__init__()
        self.backgrounds_manager: "backgrounds_manager.BackgroundsManager" = backgrounds_manager.BackgroundsManager(
            self
        )
        self.mouse_manager: "mouse_manager.StageMouseManager" = mouse_manager.StageMouseManager(self)
        self.ask: "ask.Ask" = ask.Ask(self)
        self.is_display_initialized: bool = False
        self._fps: int = 60
        self._key_pressed: bool = False
        self._animated: bool = False
        self._is_filled: bool = False
        self._orientation: int = 0
        self._static: bool = False
        self._speed: int = 1  # All tokens are acting on n:th frame with n = self.speed
        self._default_is_filled = False
        self._default_fill_color = None
        self._default_border_color = None
        self._default_border = None
        self.is_running: bool = True
        self.is_listening: bool = True
        self.frame: int = 0
        self.clock: pygame.time.Clock = pygame.time.Clock()
        if not app.App.init:
            app.App.init = True
            self.app: "app.App" = app.App("miniworldmaker")
            app.App.running_app = self.app
            app.App.running_board = self
            app.App.running_boards.append(self)
        else:
            self.app = app.App.running_app
        self.music: "board_music_manager.BoardMusicManager" = board_music_manager.BoardMusicManager(self.app)
        self.sound: "board_sound_manager.BoardSoundManager" = board_sound_manager.BoardSoundManager(self.app)
        self.background = background_mod.Background(self)
        self.background.update()
        self.collision_manager: "coll_manager.BoardCollisionManager" = coll_manager.BoardCollisionManager(self)
        self.timed_objects: list = []
        self.app.event_manager.to_event_queue("setup", None)
        self.dynamic_tokens = pygame.sprite.Group()
        self._registered_methods = []
        self.tokens_fixed_size = False
        self.container_width = self.camera.get_viewport_width_in_pixels()
        self.container_height = self.camera.get_viewport_height_in_pixels()
        self.app.container_manager.add_topleft(self)

    def _create_event_manager(self):
        return event_manager.BoardEventManager(self)

    def is_position_on_the_board(self, pos):
        """Checks if position is on the board.

        Returns:
            True, if Position is on the board.
        """
        if 0 <= pos[0] < self.boundary_x and 0 <= pos[1] < self.boundary_y:
            return True
        else:
            return False

    is_position_on_board = is_position_on_the_board
    contains_position = is_position_on_the_board

    def contains_rect(self, rect: Union[tuple, pygame.Rect]):
        """Detects if rect is completely on the board.
        
        Args:
            rect: A rectangle as tuple (top, left, width, height)
        """
        rect = board_rect.Rect.create(rect)
        topleft_on_the_board = self.contains_position(rect.topleft)
        bottom_right_on_the_board = self.contains_position(rect.bottomright)
        return topleft_on_the_board or bottom_right_on_the_board

    def setup_board(self):
        # Implemented in TiledBoards
        pass

    @property
    def speed(self) -> int:
        """speed defines how often the method ``act()`` will be called.  

        If e.g. ``speed = 30``, the game logic will be called every 30th-frame.

        .. note::

          You can adjust the frame-rate with ``board.fps``

        Examples:

            Set speed and fps.

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                board.size = (120,210)

                @board.register
                def on_setup(self):
                    board.fps = 1
                    board.speed = 3
                    
                @board.register
                def act(self):

                board.run()

        Output:

            ```
            3
            6
            9
            12
            15
            ```        
        """
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    @property
    def fps(self) -> int:
        """
        Frames per second shown on the screen.

        This controls how often the screen is redrawn. However, the game logic
        can be called more often or less often independently of this with ``board.speed.``

        Examples:

            .. code-block:: python

                board.speed = 10
                board.fps = 24
                def act(self):
                    nonlocal i
                    i = i + 1
                    if board.frame == 120:
                        test_instance.assertEqual(i, 13)
                        test_instance.assertEqual(board.frame, 120)
        """
        return self._fps

    @fps.setter
    def fps(self, value: int):
        self._fps = value

    @property
    def width(self) -> int:
        """Gets width of board in pixels.

        (for tiledboard: columns * tile_size)
        """
        return self.container_width

    @property
    def height(self) -> int:
        """Gets height of board in pixels.

        (for `tiledboard`: rows * tile_size)
        """
        return self.container_height

    @property
    def boundary_x(self) -> int:
        """The x-boundary (defaults to view_size)"""
        return self.camera.boundary_x

    @boundary_x.setter
    def boundary_x(self, value: int):
        self.camera.boundary_x = value

    @property
    def boundary_y(self) -> int:
        """The y-boundary (defaults to view_size)"""
        return self.camera.boundary_y

    @boundary_y.setter
    def boundary_y(self, value: int):
        self.camera.boundary_y = value

    @property
    def viewport_width(self) -> int:
        return self.camera.viewport_width

    @viewport_width.setter
    def viewport_width(self, value: int):
        self.camera.viewport_width = value

    @property
    def viewport_height(self) -> int:
        """The y-boundary (defaults to view_size)"""
        return self.camera.viewport_height

    @viewport_height.setter
    def viewport_height(self, value: int):
        self.camera.viewport_height = value

    @property
    def columns(self) -> int:
        return self.camera.viewport_width

    @columns.setter
    def columns(self, value: int):
        self.setup_board()
        self.camera.viewport_width = value
        self.boundary_x = value

    @property
    def rows(self) -> int:

        return self.camera.viewport_height

    @rows.setter
    def rows(self, value: int):
        self.setup_board()
        self.viewport_height = value
        self.boundary_y = value

    def borders(self, value: Union[tuple, "board_position.Position", pygame.Rect]) -> list:
        """Gets all borders from a source (`Position` or `Rect`).

        Args:
            value: Position or rect

        Returns:
            A list of borders, e.g. ["left", "top"], if rect is touching the left a top border.

        """
        pass

    @property
    def camera_x(self):
        return self.camera.x

    @camera_x.setter
    def camera_x(self, value):
        self.camera.x = value

    @property
    def camera_y(self):
        return self.camera.y

    @camera_y.setter
    def camera_y(self, value):
        self.camera.y = value

    @property
    def tile_size(self) -> int:
        """Tile size of each tile, if board has tiles

        Returns:
            The tile-size in pixels.
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value: int):
        self.set_tile_size(value)

    def set_tile_size(self, value):
        self._tile_size = value
        self.camera.reload_camera()
        self.background.set_dirty("all", background_mod.Background.RELOAD_ACTUAL_IMAGE)

    @property
    def size(self) -> tuple:
        """Set the size of board

        Examples:

          Create a board with 800 columns and 600 rows:

          .. code-block:: python

            board = miniworldmaker.PixelBoard()
            board.size = (800, 600)
        """
        return self.boundary_x, self.boundary_y

    @size.setter
    def size(self, value: tuple):
        self.boundary_x = value[0]
        self.boundary_y = value[1]
        self.viewport_width = value[0]
        self.viewport_height = value[1]

    @property
    def default_fill_color(self):
        """Set default fill color for borders and lines"""
        return self._default_fill_color

    @default_fill_color.setter
    def default_fill_color(self, value):
        self._default_fill_color = color.Color(value).get()

    def default_fill(self, value):
        """Set default fill color for borders and lines"""
        self._is_filled = value
        if self.default_is_filled is not None and self.default_is_filled:
            self._default_fill_color = color.Color(value).get()

    @property
    def default_is_filled(self):
        return self._default_is_filled

    @default_is_filled.setter
    def default_is_filled(self, value):
        self.default_fill(value)

    @property
    def default_stroke_color(self):
        """Set default stroke color for borders and lines. (equivalent to border-color)"""
        return self.default_border_color

    @default_stroke_color.setter
    def default_stroke_color(self, value):
        """Set default stroke color for borders and lines. (equivalent to border-color)"""
        self.default_border_color = value

    @property
    def default_border_color(self):
        """Set default border color for borders and lines.

        .. note::

          ``board.default_border_color`` does not have an effect, if no border is set.

            You must also set ``board.border`` > 0.

        Examples:

            Create tokens with and without with border

            .. code-block:: python

                from miniworldmaker import *

                board = Board(210,80)
                board.default_border_color = (0,0, 255)
                board.default_border = 1

                t = Token((10,10))

                t2 = Token ((60, 10))
                t2.border_color = (0,255, 0)
                t2.border = 5 # overwrites default border

                t3 = Token ((110, 10))
                t3.border = None # removes border

                t4 = Token ((160, 10))
                t4.add_costume("images/player.png") # border for sprite

                board.run()

            Output:

            .. image:: ../_images/border_color.png
                :width: 200px
                :alt: borders

        """
        return self._default_border_color

    @default_border_color.setter
    def default_border_color(self, value):
        self._default_border_color = value

    @property
    def default_border(self):
        """Sets default border color for tokens

        .. note::

          You must also set a border for token.

        Examples:

            Set default border for tokens:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(210,80)
                board.default_border_color = (0,0, 255)
                board.default_border = 1

                t = Token((10,10))

                board.run()
        """
        return self._default_border

    @default_border.setter
    def default_border(self, value):
        self._default_border = value

    @property
    def tokens(self) -> pygame.sprite.LayeredDirty:
        """A list of all tokens registered to the board."""
        return self._tokens

    @property
    def backgrounds(self) -> list:
        """Returns all backgrounds of the board as list."""
        return self.backgrounds_manager.backgrounds

    @property
    def background(self) -> "background_mod.Background":
        """Returns the current background"""
        return self.get_background()

    def get_background(self) -> "background_mod.Background":
        """Returns the current background"""
        return self.backgrounds_manager.background

    @background.setter
    def background(self, source):
        if isinstance(source, appearance.Appearance):
            self.backgrounds_manager.background = source
        else:
            self.backgrounds_manager.add_background(source)

    def switch_background(self, background: Union[int, Type["appearance.Appearance"]]) -> "background_mod.Background":
        """Switches the background

        Args:
            background: The index of the new background or an Appearance.
                If index = -1, the next background will be selected

        Examples:

            Switch between different backgrounds:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                token = Token()

                board.add_background("images/1.png")
                board.add_background((255, 0, 0, 255))
                board.add_background("images/2.png")

                @timer(frames = 40)
                def switch():
                    board.switch_background(0)

                @timer(frames = 80)
                def switch():
                    board.switch_background(1)

                @timer(frames = 160)
                def switch():
                    board.switch_background(2)

                board.run()

            Output:

            .. image:: ../_images/switch_background.png
                :width: 100%
                :alt: Switch background

        Returns:
            The new background

        """
        return self.backgrounds_manager.switch_appearance(background)

    def remove_background(self, background=None):
        """Removes a background from board

        Args:
            background: The index of the new background. Defaults to -1 (last background) or an Appearance
        """
        return self.backgrounds_manager.remove_appearance(background)

    def set_background(self, source: Union[str, tuple]) -> "background_mod.Background":
        """Adds a new background to the board

        If multiple backgrounds are added, the last adds background will be set as active background.

        Args:
            source: The path to the first image of the background or a color (e.g. (255,0,0) for red or
                    "images/my_background.png" as path to a background.

        Examples:

            Add multiple Backgrounds:

            .. code-block:: pythonlist

                from miniworldmaker import *

                board = Board()
                board.add_background((255, 0 ,0)) # red
                board.add_background((0, 0 ,255)) # blue
                board.run() # Shows a blue board.

        Returns:
            The new created background.
        """
        return self.backgrounds_manager.set_background(source)

    def add_background(self, source: Union[str, tuple]) -> "background_mod.Background":
        """Adds a new background to the board

        If multiple backgrounds are added, the last adds background will be set as active background.

        Args:
            source: The path to the first image of the background or a color (e.g. (255,0,0) for red or
                    "images/my_background.png" as path to a background.

        Examples:

            Add multiple Backgrounds:

            .. code-block:: pythonlist

                from miniworldmaker import *

                board = Board()
                board.add_background((255, 0 ,0)) # red
                board.add_background((0, 0 ,255)) # blue
                board.run() # Shows a blue board.

        Returns:
            The new created background.
        """
        return self.backgrounds_manager.add_background(source)

    def start(self):
        """Starts the board, if board is not running."""
        self.is_running = True

    def stop(self, frames=0):
        """Stops the board.

        Args:
            frames (int, optional): If ``frames`` is set, board will be stopped in n frames. . Defaults to 0.
        """
        if frames == 0:
            self.is_running = False
        else:
            timer.ActionTimer(frames, self.stop, 0)

    def start_listening(self):
        self.is_listening = True

    def stop_listening(self):
        self.is_listening = False

    def clear(self):
        """Alias of ``clean``

        see:
        :py:meth:`Board.clean`
        """
        self.clean()

    def clean(self):
        """removes all tokens

        Examples:

            Clear a board:

            .. code-block:: python

                from miniworldmaker import *
                import random

                board = Board()

                for i in range(50):
                    Token((random.randint(0,board.width), random.randint(0,board.height)))

                @timer(frames = 50)
                def clean():
                    board.clear()

                board.run()

            Output:

            .. image:: ../_images/clear.png
                :width: 100%
                :alt: Clean board
        """
        for token in self.tokens:
            token.remove()

    def run(self, fullscreen: bool = False, fit_desktop: bool = False, replit: bool = False, event=None, data=None):
        """
        The method show() should always be called at the end of your program.
        It starts the mainloop.

        Examples:

            A minimal miniworldmaker-program:

            .. code-block:: python

                from miniworldmaker import *
                board = TiledBoard()
                token = Token()
                board.run()

            Output:

            .. image:: ../_images/min.png
                :width: 200px
                :alt: Minimal program

        """
        self.app.prepare_mainloop()
        if hasattr(self, "on_setup"):
            self.on_setup()
        self.init_display()
        self.is_running = True
        if event:
            self.app.event_manager.to_event_queue(event, data)
        self.app.run(self.image, fullscreen=fullscreen, fit_desktop=fit_desktop, replit=replit)

    def init_display(self):
        if not self.is_display_initialized:
            self.is_display_initialized = True
            self.background.set_dirty("all", self.background.LOAD_NEW_IMAGE)

    def play_sound(self, path: str):
        """plays sound from path"""
        self.app.sound_manager.play_sound(path)

    def stop_sounds(self):
        self.app.sound_manager.stop()

    def play_music(self, path: str):
        """plays a music from path

        Args:
            path: The path to the music

        Returns:

        """
        self.music.play(path)

    def stop_music(self):
        """stops a music

        Returns:

        """
        self.music.stop()

    def get_mouse_position(self) -> Union["board_position.Position", None]:
        """
        Gets the current mouse_position

        Returns:
            Returns the mouse position if mouse is on the board. Returns None otherwise

        Examples:

            Create circles at current mouse position:


            .. code-block:: python

                from miniworldmaker import *

                board = PixelBoard()

                @board.register
                def act(self):
                    c = Circle(board.get_mouse_position(), 40)
                    c.color = (255,255,255, 100)
                    c.border = None

                board.run()

            Output:

            .. image:: ../_images/mousepos.png
                :width: 200px
                :alt: Circles at mouse-position


        """
        return self.mouse_manager.mouse_position

    def get_mouse_x(self) -> int:
        """Gets x-coordinate of mouse-position"""
        if self.mouse_manager.mouse_position:
            return self.mouse_manager.mouse_position[0]
        else:
            return 0

    def get_mouse_y(self) -> int:
        """Gets y-coordinate of mouse-position"""
        if self.mouse_manager.mouse_position:
            return self.mouse_manager.mouse_position[1]
        else:
            return 0

    def get_prev_mouse_position(self):
        """gets mouse-position of last frame"""
        return self.mouse_manager.prev_mouse_position

    def is_mouse_pressed(self) -> bool:
        """Returns True, if mouse is pressed"""
        return self.mouse_manager.mouse_left_is_clicked() or self.mouse_manager.mouse_left_is_clicked()

    def is_mouse_left_pressed(self) -> bool:
        """Returns True, if mouse left button is pressed"""
        return self.mouse_manager.mouse_left_is_clicked()

    def is_mouse_right_pressed(self) -> bool:
        """Returns True, if mouse right button is pressed"""
        return self.mouse_manager.mouse_right_is_clicked()

    def send_message(self, message, data=None):
        """Sends broadcast message

        A message can be received by the board or any token on board
        """
        self.app.event_manager.to_event_queue("message", message)

    def quit(self, exit_code=0):
        """quits app and closes the window"""
        self.app.quit(exit_code)

    def reset(self):
        """Resets the board
        Creates a new board with init-function - recreates all tokens and actors on the board.

        Examples:

            Restarts flappy the bird game after collision with pipe:

            .. code-block:: python

              def on_sensing_collision_with_pipe(self, other, info):
                  self.board.is_running = False
                  self.board.reset()
        """
        self.app.event_manager.event_queue.clear()
        for background in self.backgrounds:
            self.backgrounds_manager.remove_appearance(background)
        self.clean()
        if hasattr(self, "on_setup"):
            self.on_setup()

    def switch_board(self, new_board: "Board"):
        """Switches to another board

        Args:
            new_board (Board): _description_
        """
        self.stop()
        self.stop_listening()
        # for background in self.backgrounds:
        #    self.backgrounds_manager.remove_appearance(background)
        self.app.event_manager.event_queue.clear()
        self.app.container_manager.switch_board(new_board)
        new_board.init_display()
        new_board.is_running = True
        new_board.reset()
        new_board.background.set_dirty("all", 2)
        new_board.start_listening()

    def get_color_from_pixel(self, position: "board_position.Position") -> tuple:
        """
        Returns the color at a specific position

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board((100,60))

                @board.register
                def on_setup(self):
                    self.add_background((255,0,0))
                    print(self.get_color_from_pixel((5,5)))

                board.run()

            Output: (255, 0, 0, 255)

            .. image:: ../_images/get_color.png
                :width: 100px
                :alt: get color of red screen

        Args:
            position: The position to search for

        Returns:
            The color

        """
        position = board_position.Position.create(position)
        return self.app.window.surface.get_at(position.to_int())

    def get_from_pixel(self, position: Union["board_position.Position", Tuple]) -> Optional["board_position.Position"]:
        """Gets Position from pixel

        PixelBoard: the pixel position is returned
        TiledBoard: the tile-position is returned

        :param position: Position as pixel coordinates
        :return: The pixel position, if position is on the board, None if position is not on Board.
        """
        column = position[0]
        row = position[1]
        position = board_position.Position(column, row)
        if column < self.container_width and row < self.container_height:
            return position
        else:
            return None

    def get_board_position_from_pixel(self, pixel):
        """
        Alias for get_from_pixel
        """
        return self.get_from_pixel(pixel)

    def to_pixel(self, position):
        x = position[0]
        y = position[1]
        return x, y

    def on_setup(self):
        """Overwrite or register this method to call `on_setup`-Actions
        """
        pass

    def __str__(self):
        return "{0} with {1} columns and {2} rows".format(self.__class__.__name__, self.columns, self.rows)

    @property
    def container_width(self) -> int:
        """
        The width of the container
        """
        return self.camera.get_viewport_width_in_pixels()

    @property
    def container_width(self) -> int:
        """
        The width of the container
        """
        return self.camera.get_viewport_width_in_pixels()

    @container_width.setter
    def container_width(self, value):
        self._container_width = value
        self.on_change()

    @property
    def container_height(self) -> int:
        """
        The height of the container
        """
        return self.camera.get_viewport_height_in_pixels()

    @container_height.setter
    def container_height(self, value):
        self._container_height = value
        self.on_change()

    @property
    def has_background(self) -> bool:
        return self.backgrounds_manager.has_appearance()

    @property
    def registered_events(self) -> set:
        return self.event_manager.registered_events

    @registered_events.setter
    def registered_events(self, value):
        return  # setter is defined so that board_event_manager is not overwritten by board parent class container

    def add_to_board(self, token, position: tuple):
        """Adds a Token to the board.
        Is called in __init__-Method if position is set.

        Args:
            token: The token, which should be added to the board.
            position: The position on the board where the actor should be added.
        """
        self.get_token_connector(token).add_token_to_board()

    def detect_tokens(self, position: Union["board_position.Position", Tuple[float, float]]) -> List["token_mod.Token"]:
        """Gets all tokens which are found at a specific position.

        Args:
            position: Position, where tokens should be searched.

        Returns:
            A list of tokens

        Examples:

          Get all tokens at mouse position:

          .. code-block:: python

              position = board.get_mouse_position()
              tokens = board.get_tokens_by_pixel(position)

        """
        # overwritten in tiled_board_sensor
        return cast(List["token_mod.Token"],
                    [token for token in self.tokens if token.board_sensor.detect_point(position)])

    get_tokens_at_position = detect_tokens

    def get_tokens_from_pixel(self, pixel: Union["board_position.Position", Tuple[float, float]]):
        return self.detect_tokens(pixel)  # overwritten in tiled_board

    @property
    def image(self) -> pygame.Surface:
        """The current displayed image"""
        return self.backgrounds_manager.image

    def repaint(self):
        self.background.repaint()  # called 1/frame in container.repaint()

    def update(self):
        """The mainloop, called once per frame.

        Called in app.update() when update() from all containers is called.
        """
        if self.is_running or self.frame == 0:
            # Acting for all actors@static
            if self.frame > 0 and self.frame % self.speed == 0:
                self._act_all()
            self.collision_manager.handle_all_collisions()
            self.mouse_manager.update_positions()
            if self.frame == 0:
                self.init_display()
            # run animations
            self.background.update()
            self.background._update_all_costumes()  # @TODO: Update costumes for animated costumes, performance
            self._tick_timed_objects()
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self.event_manager.executed_events.clear()

    def _act_all(self):
        """Overwritten in subclasses, e.g. physics_board"""
        self.event_manager.act_all()

    def _tick_timed_objects(self):
        [obj.tick() for obj in self.timed_objects]

    def handle_event(self, event, data=None):
        """
        Event handling

        Args:
            event (str): The event which was thrown, e.g. "key_up", "act", "reset", ...
            data: The data of the event (e.g. ["S","s"], (155,3), ...
        """
        self.event_manager.handle_event(event, data)

    def register(self, method: callable) -> callable:
        """
        Used as decorator
        e.g.
        @register
        def method...
        """
        self._registered_methods.append(method)
        bound_method = board_inspection.BoardInspection(self).bind_method(method)
        self.event_manager.register_event(method.__name__, self)
        return bound_method

    def unregister(self, method: callable):
        self._registered_methods.remove(method)
        board_inspection.BoardInspection(self).unbind_method(method)

    @property
    def fill_color(self):
        return self.background.fill_color

    @fill_color.setter
    def fill_color(self, value):
        self.background.fill(value)

    # Alias
    color = fill_color

    def direction(self, point1, point2):
        pass

    @staticmethod
    def distance_to(pos1: "board_position.Position",
                    pos2: "board_position.Position"):
        pos1 = board_position.Position.create(pos1)
        pos2 = board_position.Position.create(pos2)
        if type(pos2) == board_position.Position:
            return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)
        elif type(pos2) == tuple:
            return math.sqrt((pos1.x - pos2[0]) ** 2 + (pos1.y - pos2[1]) ** 2)

    @staticmethod
    def direction_to(pos1: "board_position.Position",
                     pos2: "board_position.Position") -> "board_direction.Direction":
        return board_direction.Direction.from_two_points(pos1, pos2)
