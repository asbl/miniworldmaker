from typing import Type, Union, Tuple, ValuesView

import pygame

import inspect
from typing import List, Tuple, Union

import pygame
import os

import miniworldmaker.appearances.background as background

import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_rect as board_rect
import miniworldmaker.appearances.backgrounds_manager as backgrounds_manager
import miniworldmaker.boards.board_manager.board_collision_manager as coll_manager
import miniworldmaker.boards.board_manager.board_event_manager as event_manager
import miniworldmaker.boards.board_manager.board_mouse_manager as mouse_manager
import miniworldmaker.boards.token_connectors.token_connector as token_connector


import miniworldmaker.dialogs.ask as ask
import miniworldmaker.tokens.token as token_module
import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.background as background
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.boards.board_base as board_base
import miniworldmaker.boards.token_connectors.pixel_board_connector as pixel_board_connector
import miniworldmaker.tools.color as color
import miniworldmaker.tools.board_inspection as board_inspection
import miniworldmaker.tools.timer as timer
from miniworldmaker.base import app
from miniworldmaker.exceptions.miniworldmaker_exception import (
    BoardArgumentsError,
    NotImplementedOrRegisteredError,
)
import miniworldmaker.board_positions.board_position as board_position

class Board(board_base.BaseBoard):
    """A board is a playing field on which tokens can move.

    A board has a `background` and provides basic functions for the positioning of
    tokens and for the colission detection of tokens, which can be queried via the sensors of the tokens.

    You can create a custom board by inherit from Board or one of Board subclasses (e.g. TiledBoard or  PhysicsBoard)
    or by creating a board-object:

    *Board*

    A board for pixel accurate games.

    * The position of a token on a Board is the pixel at topleft of token.

    * New tokens are created with top-left corner of token rect at position.

    * Two tokens collide when their sprites overlap.

    .. image:: ../_images/asteroids.jpg
        :width: 100%
        :alt: Asteroids

    Creating a Board:

    .. code-block:: python

        from miniworldmaker import *

        myboard = Board()

    *Tiledboard*

    A Board for Games based on Tiles (Like Rogue-Like RPGs).

    * Every token on a TiledBoard has the size of exactly on one Tile. (If your tile_size is 40, every token has the size 40x40. )

    * The `position` of a token (*mytoken.position*) corresponds to the tile on which it is placed.

    * Two tokens **collide** when they are on the same tile.

    .. image:: ../_images/tiled_board.jpg
        :width: 100%
        :alt: TiledBoard

    Creating a TiledBoard:

    .. code-block:: python

        from miniworldmaker import *

        myboard = TiledBoard()

    Examples:

        Creating a TiledBoard Object:

        .. code-block:: python

            from miniworldmaker import *

            myboard = TiledBoard()
            myboard.columns = 30
            myboard.rows = 20
            myboard.tile_size = 20


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

            myboard = Board()
            myboard.columns = 300
            myboard.rows = 200

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
        columns: columns of new board (default: 40)
        rows: rows of new board (default:40)
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
        self.event_manager: event_manager.BoardEventHandler = event_manager.BoardEventHandler(self)
        super().__init__()
        self.backgrounds_manager: "backgrounds_manager.BackgroundsManager" = backgrounds_manager.BackgroundsManager(
            self
        )
        self.mouse_manager: "mouse_manager.BoardMouseManager" = mouse_manager.BoardMouseManager(self)
        self.ask: "ask.Ask" = ask.Ask(self)
        self._is_setup: bool = False
        self._fps: int = 60
        self._key_pressed: bool = False
        self._animated: bool = False
        self._orientation: int = 0 
        self._static: bool = False
        self._speed: int = 1  # All tokens are acting on n'th frame with n = self.speed
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
            app.App.board = self
        else:
            self.app = app.App.running_app
        self.background = background.Background(self)
        self.background.update()
        self.collision_manager: "coll_manager.BoardCollisionHandler" = coll_manager.BoardCollisionHandler(self)
        self.timed_objects: list = []
        self.app.event_manager.to_event_queue("setup", self)
        self.dynamic_tokens = set()
        self._registered_methods = []
        self.tokens_fixed_size = False
        self._container_width = self.camera.get_viewport_width_in_pixels()
        self._container_height = self.camera.get_viewport_height_in_pixels() 
        self.app.container_manager.add_topleft(self)

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
                    print(board.frame)

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
                    print(board.frame, i)
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

        (for tiledboard: rows * tile_size)
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
        print("changed rows")
        self.setup_board()
        self.viewport_height = value
        self.boundary_y = value     

    def borders(self, value: Union[tuple, "board_position.Position", pygame.Rect]) -> list:
        """
        Gets all borders a rect is touching

        Args:
            rect: The rect

        Returns: A list of borders, e.g. ["left", "top", if rect is touching the left a top border.

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
            int: The tile-size in pixels.
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value: int):
        self.set_tile_size(value)

    def set_tile_size(self, value):
        self._tile_size = value
        self.app.window.resize()
        self.background.set_dirty("all", background.Background.RELOAD_ACTUAL_IMAGE)

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
        if self.default_is_filled != None and self.default_is_filled != False:
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
    def backgrounds(self):
        """Returns the background of board."""
        return self.backgrounds_manager.backgrounds
    
    @property
    def background(self):
        """Returns the background of board."""
        return self.get_background()

    def get_background(self):
        return self.backgrounds_manager.background
    
    @background.setter
    def background(self, source):
        if isinstance(source, appearance.Appearance):
            self.backgrounds_manager.background = source
        else:
            self.backgrounds_manager.add_background(source)

    def switch_background(self, background: Union[int, Type["appearance.Appearance"]]) -> "background.Background":
        """Switches the background of board

        Args:
            index: The index of the new background. If index=-1, the next background will be selected

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
        self.backgrounds_manager.switch_background(background)

    def remove_background(self, background=None):
        """Removes a background from board

        Args:
            index: The index of the new background. Defaults to -1 (last background)
        """
        self.backgrounds_manager.remove_background()

    def add_background(self, source: Union[str, tuple]) -> "background.Background":
        """
        Adds a new background to the board

        Args:
            source: The path to the first image of the background or a color

        Examples:

            Multiple Backgrounds:

            .. code-block:: python

                board = miniworldmaker.TiledBoard()
                ...
                board.add_background("images/soccer_green.jpg")
                board.add_background("images/space.jpg")

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
        The method show() should always called at the end of your program.
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
        if not self._is_setup and hasattr(self, "on_setup") and callable(getattr(self, "on_setup")):
            self.app._prepare_mainloop()
            self.event_manager.handle_event("setup", None)
            self._is_setup = True
            self.app.event_manager.to_event_queue("setup", self)
        if event:
            self.app.event_manager.to_event_queue(event, data)
        self.app.run(self.image, fullscreen=fullscreen, fit_desktop=fit_desktop, replit=replit)

    def play_sound(self, path: str):
        """plays sound from path"""
        self.app.sound_manager.play_sound(path)

    def play_music(self, path: str):
        """plays a music from path

        Args:
            path: The path to the music

        Returns:

        """
        self.app.sound_manager.play_music(path)

    def get_mouse_position(self) -> Union["board_position.Position", None]:
        """
        Gets the current mouse_position

        Returns:
            Returns the mouse position if mouse is on board. Returns None otherwise

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

        A message can received by the board or any token on board
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


    def switch_board(self, new_board: "board_base.BaseBoard"):
        """Switches to another board

        Args:
            new_board (board_base.BaseBoard): _description_
        """
        self.stop()
        self.stop_listening()
        #for background in self.backgrounds:
        #    self.backgrounds_manager.remove_appearance(background)
        #self.clean()
        self.app.event_manager.event_queue.clear()
        self.app.container_manager.switch_container(self, new_board)
        self.app.switch_board(new_board)
        new_board.start()
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
        from __future__ import annotations

        :alt: get color of red screen



        Args:
            position: The position to search for

        Returns: The color

        """
        position = board_position.Position.create(position)
        return self.app.window.surface.get_at(position.to_int())

    def get_from_pixel(self, position : Union["board_position.Position", Tuple]) -> "board_position.Position":
        """Gets Position from pixel

        PixelBoard: the pixel position is returned
        TiledBoard: the tile-position is returned

        :param position: Position as pixel coordinates
        :return: The pixel position, if position is on board, None if position is not on Board.
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
    def container_height(self) -> int:
        """
        The height of the container
        """
        return self.camera.get_viewport_height_in_pixels()

    @property
    def has_background(self) -> bool:
        return self.backgrounds_manager.has_background

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
        self.get_token_connector(token).add_token_to_board(token, position)

    def get_tokens_from_pixel(self, pixel: tuple) -> list:
        """Gets all tokens by Pixel.

        Args:
            pixel: the pixel-coordinates

        Returns:
            A list of tokens

        Examples:

          Get all tokens at mouse position:

          .. code-block:: python

              position = board.get_mouse_position()
              tokens = board.get_tokens_by_pixel(position)

        """
        return [token for token in self.tokens if token.sensing_point(pixel)]

    def get_tokens_at_position(self, position) -> list:
        """Alias for ``get_tokens_from_pixel``
        """
        return self.get_tokens_from_pixel(position)

    @property
    def image(self) -> pygame.Surface:
        """The current displayed image"""
        return self.backgrounds_manager.image

    def repaint(self):
        self.background.repaint()  # called 1/frame in container.repaint()

    def update(self):
        """This is the board-mainloop()
        Called in app.update() when update() vom all containers is called.
        """
        if self.is_running or self.frame == 0:
            # Acting for all actors@static
            if self.frame > 0 and self.frame % self.speed == 0:
                self.act_all()
            self.collision_manager.handle_all_collisions()
            self.mouse_manager.update_positions()
            # run animations
            self.background._update_all_costumes()
            self.background.update()
            self._tick_timed_objects()
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self.event_manager.executed_events.clear()

    def act_all(self):
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

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.backgrounds_manager.find_colors(rect, color, threshold)

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
        

    