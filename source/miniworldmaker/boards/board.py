from typing import Type, Union

import pygame

import miniworldmaker.appearances.appearance as appearance
import miniworldmaker.appearances.background as background
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.boards.board_base as board_base
import miniworldmaker.boards.token_connectors.pixel_board_connector as pixel_board_connector
import miniworldmaker.tools.color as color
import miniworldmaker.tools.timer as timer


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
    def rows(self) -> int:
        """The number of rows"""
        return self._rows

    @rows.setter
    def rows(self, value: int):
        self._rows = value
        self.app.window.dirty = 1
        self.background.reload_transformations_after("all")

    @property
    def columns(self) -> int:
        """The number of columns"""
        return self._columns

    @columns.setter
    def columns(self, value: int):
        self._columns = value
        self.app.window.dirty = 1
        self.background.reload_transformations_after("all")

    @property
    def size(self) -> tuple:
        """Set the size of board

        Examples:

          Create a board with 800 columns and 600 rows:

          .. code-block:: python

            board = miniworldmaker.PixelBoard()
            board.size = (800, 600)
        """
        return (self.columns, self.rows)

    @size.setter
    def size(self, value: tuple):
        self.columns = value[0]
        self.rows = value[1]
        self.background.reload_transformations_after("all")
        self.app.window.dirty = 1

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
    def background(self):
        """Returns the background of board."""
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
            self.app.event_manager.send_event_to_containers("setup", self)
        if event:
            self.app.event_manager.send_event_to_containers(event, data)
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
        return self.position_manager.mouse_position

    def get_mouse_x(self) -> int:
        """Gets x-coordinate of mouse-position"""
        if self.position_manager.mouse_position:
            return self.position_manager.mouse_position[0]
        else:
            return 0

    def get_mouse_y(self) -> int:
        """Gets y-coordinate of mouse-position"""
        if self.position_manager.mouse_position:
            return self.position_manager.mouse_position[1]
        else:
            return 0

    def get_prev_mouse_position(self):
        """gets mouse-position of last frame"""
        return self.position_manager.prev_mouse_position

    def is_mouse_pressed(self) -> bool:
        """Returns True, if mouse is pressed"""
        if pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

    def send_message(self, message, data=None):
        """Sends broadcast message

        A message can received by the board or any token on board
        """
        self.app.event_manager.send_event_to_containers("message", message)

    def screenshot(self, filename: str = "screenshot.jpg"):
        """Creates a screenshot in given file.

        Args:
            filename: The location of the file. The folder must exist. Defaults to "screenshot.jpg".
        """

        pygame.image.save(self.app.window.surface, filename)

    def quit(self, exit_code=0):
        """quits app and closes the window"""
        self.app.quit(exit_code)

    def switch_board(self, new_board: "board_base.BaseBoard"):
        """Switches to another board

        Args:
            new_board (board_base.BaseBoard): _description_
        """
        self.event_manager.handle_switch_board_event(new_board)

    def get_token_connector(self, token):
        return pixel_board_connector.PixelBoardConnector(self, token)

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

        Returns: The color

        """
        position = board_position.Position.create(position)
        return self.app.window.surface.get_at(position.to_int())

    def get_from_pixel(self, position):
        column = position[0]
        row = position[1]
        return column, row

    def to_pixel(self, position):
        x = position[0]
        y = position[1]
        return x, y
