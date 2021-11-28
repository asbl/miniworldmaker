from typing import Union
from typing import Type
import pygame
import inspect
from miniworldmaker.app import app
from miniworldmaker.appearances.appearance import Appearance
from miniworldmaker.appearances.background import Background
from miniworldmaker.board_positions import board_position_factory
from miniworldmaker.board_positions import board_rect_factory
from miniworldmaker.board_positions import board_position
from miniworldmaker.boards.board_handler.board_event_handler import BoardEventHandler
from miniworldmaker.boards.board_handler.board_collision_handler import BoardCollisionHandler
from miniworldmaker.boards.board_handler.board_view_handler import BoardViewHandler
from miniworldmaker.boards.board_handler.board_position_handler import BoardPositionHandler
from miniworldmaker.boards.token_connectors.token_connector import TokenConnector
from miniworldmaker.containers import container
from miniworldmaker.exceptions.miniworldmaker_exception import BoardArgumentsError, BoardInstanceError
from miniworldmaker.tools import timer
from miniworldmaker.tokens import token as token_module
from miniworldmaker.tools import inspection_methods
from miniworldmaker.boards.data import import_factory
from miniworldmaker.boards.data import export_factory
from miniworldmaker.tokens.token import Token


class Board(container.Container):
    """Base Class for Boards.

    You can create a custom board by inherit one of Board subclasses or by creating a board-object:

    Examples:
        Creating a board object:

        .. code-block:: python

            board = miniworldmaker.TiledBoard()
            board.columns=20
            board.rows=8
            board.tile_size=40

        A pixel-board in follow_the_mouse.py:

        .. code-block:: python

            class MyBoard(PixelBoard):

            def on_setup(self):
                self.add_background(path="images/stone.jpg")
                Robot(position=(50, 50))


            board = MyBoard(800, 600)

        A tiled-board:

        .. code-block:: python

            board = MyBoard(columns=20, rows=8, tile_size=42, tile_margin=0)

        > See [Examples](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/1%20Costumes%20and%20Backgrounds)

    Args:
        columns: columns of new board (default: 40)
        rows: rows of new board (default:40)
    """

    subclasses = None

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size: int = 1,
                 tile_margin: int = 0,
                 background_image=None
                 ):
        if self.__class__ == Board:
            raise BoardInstanceError()
        self._tokens = pygame.sprite.LayeredDirty()
        self.event_handler = BoardEventHandler(self)
        super().__init__()
        self.view_handler = BoardViewHandler(self)
        self.position_handler = BoardPositionHandler(self)
        pygame.init()
        # public
        self.is_running: bool = True
        # protected
        self._is_setup: bool = False
        if not hasattr(self, "_fps"):
            self._fps: int = 60  # property speed
        self._key_pressed: bool = False
        self._animated: bool = False
        self._orientation: int = 0
        if type(columns) != int or type(rows) != int:
            if type(columns) == tuple:
                size = columns
                columns = size[0]
                rows = size[1]
            else:
                raise BoardArgumentsError(columns, rows)
        self._columns, self._rows, self._tile_size, self._tile_margin = columns, rows, tile_size, tile_margin
        self.frame: int = 0
        self._speed: int = 1  # All tokens are acting on n'th frame with n = self.speed
        self.clock: pygame.time.Clock = pygame.time.Clock()
        # Init graphics
        self.app: app.App = app.App("miniworldmaker")
        self.app.container_manager.add_container(self, "top_left")
        app.App.board = self
        self.view_handler.init_background(background_image)
        self.view_handler.update_background()
        self.collision_handler = BoardCollisionHandler(self)
        self.dirty: int = 1
        self.timed_objects: list = []
        self.app.event_manager.send_event_to_containers("setup", self)
        self.cache = dict()
        self.cache["token_classes"] = self.get_token_classes()  # @todo: No cache implemented yet
        self.load_from_db = False
        

    def get_token_connector(self, token):
        return TokenConnector(self, token)

    def load_board_from_db(self, file: str):
        """
        Loads a sqlite db file.
        """
        return import_factory.ImportBoardFromDB(file, self.__class__).load()

    def load_tokens_from_db(self, file: str, token_classes: list):
        return import_factory.ImportTokensFromDB(file, token_classes).load()

    def save_to_db(self, file):
        """
        Saves the current board an all actors to database.
        The file is stored as db file and can be opened with sqlite.

        Args:
            file: The file as relative location

        Returns:

        """
        export = export_factory.ExportBoardToDBFactory(file, self)
        export.remove_file()
        export.save()
        print("exported board")
        export_factory.ExportTokensToDBFactory(file, self.tokens).save()
        print("exported tokens")

    @classmethod
    def all_subclasses(cls):
        def rec_all_subs(base_cls) -> set:
            if cls.subclasses is None:
                return set(base_cls.__subclasses__()).union(
                    [s for c in base_cls.__subclasses__() for s in rec_all_subs(c)])
            else:
                return cls.subclasses

        return rec_all_subs(cls)

    def __str__(self):
        return "{0} with {1} columns and {2} rows" \
            .format(self.__class__.__name__, self.columns, self.rows)

    @property
    def container_width(self) -> int:
        """
        The width of the container
        """
        if self.view_handler.repaint_all:
            self._container_width = self.columns * self.tile_size + \
                (self.columns + 1) * self.tile_margin
        return self._container_width

    @property
    def container_height(self) -> int:
        """
        The height of the container
        """
        if self.view_handler.repaint_all:
            self._container_height = self.rows * \
                self.tile_size + (self.rows + 1) * self.tile_margin
        return self._container_height

    @property
    def speed(self) -> int:
        """
        How often are events and game logic processed?

        The game logic can be called more often or less often independently from board.fps

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
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    @property
    def has_background(self) -> bool:
        return self.view_handler.has_background

    @property
    def fps(self) -> int:
        """
        Frames per second shown on the screen.

        This controls how often the screen is redrawn. However, the game logic 
        can be called more often or less often independently of this with board.speed.

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
        """
        See container_width
        """
        return self.container_width

    @property
    def height(self) -> int:
        """
        See container_height
        """
        return self.container_height

    @property
    def window(self) -> app.App:
        """
        Gets the parent window

        Returns:
            The window

        """
        return self._window

    @property
    def rows(self) -> int:
        """
        The number of rows
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.app.window.dirty = 1
        self.view_handler.full_repaint()

    @property
    def columns(self) -> int:
        """
        The number of columns
        """
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.app.window.dirty = 1
        self.view_handler.full_repaint()

    @property
    def size(self) -> tuple:
        return (self.columns, self.rows)

    @size.setter
    def size(self, value: tuple):
        self.columns = value[0]
        self.rows = value[1]
        self.view_handler.full_repaint()
        self.app.window.dirty = 1

    @property
    def tile_size(self) -> int:
        """
        The number of columns
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value
        self.app.window.dirty = 1
        self.view_handler.full_repaint()

    @property
    def tile_margin(self) -> int:
        """
        The number of columns
        """
        return self._tile_margin

    @tile_margin.setter
    def tile_margin(self, value):
        self._tile_margin = value
        self.app.window.dirty = 1
        self.view_handler.full_repaint()

    @property
    def tokens(self) -> pygame.sprite.LayeredDirty:
        """
        A list of all tokens registered to the grid.
        """
        return self._tokens

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def registered_events(self) -> set:
        return self.event_handler.registered_events

    @registered_events.setter
    def registered_events(self, value):
        return  # @TODO setter is used so that board_event_handler is not overwritten by board parent class container

    @property
    def background(self):
        return self.view_handler.background

    def remove_from_board(self, token: token_module.Token):
        """
        removes a token from board.
        The method is called with token.remove()

        Args:
            token: The token to remove from board.

        Returns:

        """
        self.get_token_connector(token).remove_from_board(token)

    def remove_background(self, background=None):
        """Removes a background from board

        Args:
            index: The index of the new background. Defaults to -1 (last background)
        """
        self.view_handler.remove_background()

    def add_background(self, source: Union[str, tuple]) -> Background:
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
        self.view_handler.add_background(source)

    def add_to_board(self, token, position: tuple):
        """
        Adds a Token to the board.
        Is called in __init__-Method if position is set.

        Args:
            board: The board, the actor should be added
            position: The position on the board where the actor should be added.
        """
        self.get_token_connector(token).add_token_to_board(token, position)

    def blit_surface_to_window_surface(self):
        self.app.window.surface.blit(self.surface, self.rect)

    def get_colors_at_position(self, position: tuple):
        position = board_position_factory.BoardPositionFactory(self).create(position)
        return self.position_handler.get_color(position)

    def get_colors_at_line(self, line: list):
        """
        Gets all colors in a line. A line is a list of board_positions

        Args:
            line: the line

        Returns: 
            A list of all colors found at the line

        """
        colors = []
        for pos in line:
            pos = board_position_factory.BoardPositionFactory(self).create(pos)
            color_at_pos = self.get_colors_at_position(pos)
            if color_at_pos not in colors:
                colors.append(color_at_pos)
        return colors

    def get_color_at_rect(self, rect: pygame.Rect, directions=None) -> list:
        return rect.colors()

    def get_tokens_by_pixel(self, pixel: tuple) -> list:
        """Gets all tokens by Pixel.

        Args:
            pixel: the pixel-coordinates

        Returns:
            A list of tokens

        Examples:
            >>> position = board.get_mouse_position()
            >>> tokens = board.get_tokens_by_pixel(position)

        """
        return [token for token in self.tokens if token.rect.collidepoint(pixel)]

    def get_tokens_at_rect(self, rect: pygame.Rect, singleitem=False, exclude=None, token_type=None) -> Union[
            token_module.Token, list]:
        """
        Gets all Tokens which are colliding with a given rect.

        Args:
            rect: The rect
            singleitem: Should the method return a single token (faster) or all tokens at rect (slower)
            exclude: Exclude a token
            token_type: Filter return values by token type

        Returns: A single token or a list of tokens at rect

        """
        pass

    @property
    def image(self) -> pygame.Surface:
        """
        The current displayed image
        """
        return self.view_handler.image

    @property
    def surface(self):
        return self.view_handler.surface

    @surface.setter
    def surface(self, value):
        """
        Method is overwritten in subclasses
        """
        pass

    def remove_tokens_from_rect(self, rect, token_class=None, exclude=None):
        """Removes all tokens in an area

        Args:
            rect: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token_class: The class of the tokens which should be removed
            exclude: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area
        """
        board_rect = board_rect_factory.BoardRectFactory(self).create(rect)
        tokens = self.get_tokens_at_rect(board_rect)
        for token in tokens:
            if token is not None:
                [token.remove() for token in Board.filter_actor_list(tokens, token_class)]

    def start(self):
        self.is_running = True

    def stop(self, frames=1):
        """
        stops the board in n-frames
        """
        if frames == 0:
            self.is_running = False
        else:
            timer.ActionTimer(frames, self.stop, 0)

    def clear(self):
        self.clean()

    def clean(self):
        for token in self.tokens:
            token.remove()

    def reset(self):
        """Resets the board
        Creates a new board with init-function - recreates all tokens and actors on the board.

        Examples:

            Restarts flappy the bird game after collision with pipe:

            >>> def on_sensing_collision_with_pipe(self, other, info):
            >>>    self.board.is_running = False
            >>>    self.board.reset()
        """
        self.app.event_manager.send_event_to_containers("reset", self)

    def repaint(self):
        self.view_handler.repaint()

    def run(self, fullscreen=False):
        """
        The method show() should always called at the end of your program.
        It starts the mainloop.

        Examples:
            >>> my_board = Board() # or a subclass of Board
            >>> my_board.show()

        """
        if not self._is_setup:
            if hasattr(self, "setup") and callable(getattr(self, "setup")):
                self.app.event_manager.send_event_to_containers("setup", self)
            if hasattr(self, "on_setup") and callable(getattr(self, "on_setup")):
                self.app.event_manager.send_event_to_containers("setup", self)
        self.app.run(self.image, full_screen=fullscreen)

    def switch_background(self, background: Union[int, Type[Appearance]]) -> Background:
        """Switches the background of costume

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: 
            The new costume

        """
        self.view_handler.switch_background(background)

    def update(self):
        # This is the board-mainloop()
        # Called in miniworldwindow.update as container.update()
        if self.is_running or self.frame == 0:
            # Acting for all actors
            if self.frame > 0 and self.frame % self.speed == 0:
                self.act_all()
            if inspection_methods.InspectionMethods.get_instance_method(self, "on_run"):
                self.handle_on_run_method()
            self.collision_handler.handle_all_collisions()
            # run animations
            self.view_handler.update_all_costumes()
            self.view_handler.update_background()
            self._tick_timed_objects()
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self.event_handler.executed_events.clear()

    def handle_on_run_method(self):
        on_run = inspect.getsourcelines(self.on_run)[0]
        if self.frame % self.speed == 0 and self.frame != 0:
            line_number = self.frame // self.speed + 2
            if line_number < len(on_run):
                exec(on_run[line_number].strip())

    def act_all(self):
        for token in self.tokens:
            if token.board:  # is on board
                self.event_handler.handle_act_event(token)
        # If board has act method call board.act()
        method = inspection_methods.InspectionMethods.get_instance_method(
            self, "act")
        if method:
            method = inspection_methods.InspectionMethods.call_instance_method(
                self, method, None)

    def _tick_timed_objects(self):
        [obj.tick() for obj in self.timed_objects]

    def handle_event(self, event, data=None):
        """
        Event handling

        Args:
            event (str): The event which was thrown, e.g. "key_up", "act", "reset", ...
            data: The data of the event (e.g. ["S","s"], (155,3), ...
        """
        self.event_handler.handle_event(event, data)

    def play_sound(self, path: str):
        self.app.sound_manager.play_sound(path)

    def play_music(self, path: str):
        """
        plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        self.app.sound_manager.play_music(path)

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.view_handler.find_colors(rect, color, threshold)

    def get_mouse_position(self) -> Union[board_position.BoardPosition, None]:
        """
        Gets the current mouse_position

        Returns:
            Returns the mouse position if mouse is on board. Returns "None" otherwise

        Examples:
            This example shows you how to use the mouse_position

            >>> def act(self):
            >>>     mouse = self.board.get_mouse_position()
            >>>     if mouse:
            >>>         self.point_towards_position(mouse)

        """
        pos = board_position_factory.BoardPositionFactory(self).from_pixel(pygame.mouse.get_pos())
        clicked_container = self.app.container_manager.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self:
            return pos
        else:
            return None

    def get_board_position_from_pixel(self, pixel):
        return board_position_factory.BoardPositionFactory(self).from_pixel(pixel)

    def _update_event_handling(self):
        self.event_handler.update_event_handling()

    def is_position_on_board(self, position: board_position.BoardPosition) -> bool:
        return self.position_handler.is_position_on_board(position)

    def register(self, method):
        """
        Used as decorator
        e.g.
        @register
        def method...
        """
        bound_method = method.__get__(self, self.__class__)
        setattr(self, method.__name__, bound_method)
        return bound_method

    def send_message(self, message, data=None):
        self.app.event_manager.send_event_to_containers("message", message)

    def screenshot(self, filename="screenshot.jpg"):
        pygame.image.save(self.surface, filename)

    def quit(self, exit_code=0):
        self.app.quit(exit_code)

    def add_container(self, container, dock, size=None):
        return self.app.container_manager.add_container(container, dock, size)

    def switch_board(self, new_board):
        self.event_handler.handle_switch_board_event(new_board)

    def get_tokens_by_class_name(self, classname):
        return [token for token in self._tokens if token.__class__.__name__ == classname]

    def get_token_classes(self):
        return set([token.__class__ for token in self._tokens])

    def get_tokens_by_class(self, classname):
        return [token for token in self._tokens if isinstance(token, classname)]

    def find_token_class_for_name(self, classname):
        classname = classname.lower()
        for token_cls in self.get_token_classes():
            if token_cls.__name__.lower() == classname:
                return token_cls
        return None
