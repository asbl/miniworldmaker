import inspect
import os
from collections import defaultdict
from inspect import signature
from typing import Union
from typing import Type
import pygame
from miniworldmaker.app import app
from miniworldmaker.appearances import background
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect
from miniworldmaker.containers import container
from miniworldmaker.appearances import appearances
from miniworldmaker.appearances.appearance import Appearance
from miniworldmaker.physics import physics
from miniworldmaker.tools import timer
from miniworldmaker.physics import physics as physicsengine
from miniworldmaker.tokens import token as tkn
from miniworldmaker.tools import db_manager


class MetaBoard(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        #if hasattr(instance, "on_setup"):
        #    instance.on_setup()
        #if hasattr(instance, "setup"):
        #    instance.setup()
        return instance


class Board(container.Container, metaclass=MetaBoard):
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
                self.add_image(path="images/stone.jpg")
                Robot(position=(50, 50))
            
            
            board = MyBoard(800, 600)
        
        A tiled-board:

        .. code-block:: python
        
            def on_setup(self):
                self.add_image(path="images/soccer_green.jpg")
                self.player = Player(position=(3, 4))
                self.speed = 10
                stone = self.add_background(("images/stone.png"))
                stone.is_textured = True
                stone.is_scaled_to_tile = True
        
        
            board = MyBoard(columns=20, rows=8, tile_size=42, tile_margin=0)

        > See [Example](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/basics)

    Args:
        columns: columns of new board (default: 40)
        rows: rows of new board (default:40)
    """
    registered_collision_handlers_for_tokens = defaultdict(list)
    token_class_ids = defaultdict()  # class_name -> id
    token_classes = defaultdict()  # class_name -> class
    token_class_id_counter = 0
    subclasses = None
    begin_prefix = "on_touching_"
    separate_prefix = "on_separation_from_"

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 tile_size=1,
                 tile_margin=0,
                 background_image=None
                 ):

        super().__init__()
        pygame.init()
        # public
        self.registered_events = {"all"}
        self.is_running = True
        self.sound_effects = {}
        self.physics_property = physicsengine.PhysicsProperty
        # protected
        self._is_setup = False
        if not hasattr(self, "_fps"):
            self._fps = 60  # property speed
        self._tokens = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._animated = False
        self._grid = []
        self._orientation = 0
        self._repaint_all = 1
        if type(columns) != int or type(rows) != int:
            if type(columns) == tuple and type(columns[0]) == int and type(columns[0]) == int:
                columns, rows = columns[0], columns[1]
            else:
                raise TypeError("ERROR: columns and rows should be int values but types are",
                            str(type(columns)), "and", str(type(rows)))
        self._columns, self._rows, self._tile_size, self._tile_margin = columns, rows, tile_size, tile_margin
        self._grid = []
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)
        self.background = None
        self.backgrounds = appearances.Backgrounds(self.background)
        self._update_background()
        self._image = pygame.Surface((1, 1))
        self.surface = pygame.Surface((1, 1))
        self.frame = 0
        self._speed = 1 # All tokens are acting on n'th frame with n = self.speed
        self.clock = pygame.time.Clock()
        self.__last_update = pygame.time.get_ticks()
        # Init graphics
        self._app = app.App("MiniWorldMaker")
        self._app.add_container(self, "top_left")
        app.App.board = self
        self.registered_event_handlers = dict()
        self.tokens_with_eventhandler = defaultdict(list)
        self.tokens_with_collisionhandler = defaultdict(list)
        if background_image is not None:
            self.add_background(background_image)
        self.dirty = 1
        self.timed_objects = []
        self._repaint_all = 1
        self._executed_events = set()
        self.window.send_event_to_containers("setup", self)
        self.has_background = False
        if background_image is not None:
            self.add_background(background_image)
            self.has_background = True
        else: 
            self.add_background(None)
            self.has_background = False

    @classmethod
    def from_db(cls, file):
        """
        Loads a sqlite db file.
        """
        db = db_manager.DBManager(file)
        data = db.select_single_row("SELECT rows, columns, tile_size, tile_margin, board_class FROM Board")
        board = cls()
        board.rows = data[0]
        board.columns = data[1]
        board._tile_size = data[2]
        board._tile_margin = data[3]
        data = db.select_all_rows("SELECT token_id, column, row, token_class FROM token")
        if data:
            for tokens in data:
                token_class_name = tokens[3]
                token_class = tkn.Token
                class_list = tkn.Token.all_subclasses()
                for cls_obj in class_list:
                    if cls_obj.__name__ == token_class_name:
                        token_class = cls_obj
                token_class(position=(tokens[1], tokens[2]))  # Create token
        board.window.send_event_to_containers("Loaded from db", board)
        return board

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

    def _act_all(self):
        for token in self.tokens:
            if token.board:  # is on board
                self._handle_act_event(token)
        method = self._get_method(self, "act")
        if method:
            method()

    @property
    def container_width(self) -> int:
        """
        The width of the container
        """
        if self._repaint_all:
            self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
        return self._container_width

    @property
    def container_height(self) -> int:
        """
        The height of the container
        """
        if self._repaint_all:
            self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
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
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def columns(self) -> int:
        """
        The number of columns
        """
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tile_size(self) -> int:
        """
        The number of columns
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tile_margin(self) -> int:
        """
        The number of columns
        """
        return self._tile_margin

    @tile_margin.setter
    def tile_margin(self, value):
        self._tile_margin = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tokens(self) -> pygame.sprite.LayeredDirty:
        """
        A list of all tokens registered to the grid.
        """
        return self._tokens

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def remove_background(self):
        """Removes a background from board

        Args:
            index: The index of the new background. Defaults to -1 (last background)
        """
        if background != None:
            index = self.backgrounds.get_index(self.background)
            self.backgrounds.remove(index)
        else:
            self.backgrounds.remove(-1)

    def add_background(self, source: Union[str, tuple]) -> background.Background:
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
        if not self.has_background and self.background != None:
            self.remove_background()
        if source is None:
            source =  (255, 0,255,100)
        new_background = background.Background(self)

        if type(source) == str:
            new_background.add_image(source)
        elif type(source) == tuple:
            new_background.fill(source)
        if self.background is None or not self.has_background:
            self.background = new_background
            self._repaint_all = 1
            self._update_all_costumes()
            self._update_background()
        self.backgrounds.add(new_background)
        return new_background

    def add_to_board(self, token, position: board_position.BoardPosition):
        """
        Adds an actor to the board.
        Is called in __init__-Method if position is set.

        Args:
            board: The board, the actor should be added
            position: The position on the board where the actor should be added.
        """
        self.tokens.add(token)
        token.dirty = 1
        if token.init != 1:
            raise UnboundLocalError("super().__init__() was not called")
        self._register_physics_collision_handler(token)
        # Board Connectors are added in subclasses
        self._add_board_connector(token, position)

    def _add_board_connector(self, token, position):
        raise Exception(
            "You can't use class Board - You must use a specific class e.g. PixelBoard, TiledBoard or PhysicsBoard")

    def blit_surface_to_window_surface(self):
        self.window.window_surface.blit(self.surface, self.rect)

    def get_colors_at_position(self, position: Union[tuple, board_position.BoardPosition]):
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        return position.color()

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
            if type(pos) == tuple:
                pos = board_position.BoardPosition.from_tuple(pos)
            color_at_pos = pos.color()
            if color_at_pos not in colors:
                colors.append(color_at_pos)
        return colors

    def get_color_at_rect(self, rect: board_rect.BoardRect, directions=None) -> list:
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
        tkn.Token, list]:
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
        if self.background:
            self._image = self.background.image
        return self._image

    def remove_tokens_from_rect(self, rect: Union[tuple, pygame.Rect], token=None, exclude=None):
        """Removes all tokens in an area

        Args:
            rect: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be removed
            exclude: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area
        """
        if type(rect) == tuple:
            rect = pygame.Rect(rect[0], rect[1], 1, 1)
        tokens = self.get_tokens_at_rect(rect)
        if token is not None:
            [token.remove() for token in Board.filter_actor_list(tokens, token)]

    def start(self):
        self.is_running = True

    def stop(self, frames = 1):
        """
        stops the board in n-frames
        """
        if frames == 0:
            self.is_running = False
        else:
            timer.ActionTimer(frames, self.stop, 0)

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
        self.window.send_event_to_containers("reset", self)

    def repaint(self):
        if self.background:
            if self._repaint_all:
                    self.background.call_all_actions()
                    self.surface = pygame.Surface((self.container_width, self.container_height))
                    self.surface.blit(self.image, self.surface.get_rect())
            self.tokens.clear(self.surface, self.image)
            repaint_rects = self.tokens.draw(self.surface)
            self.window.repaint_areas.extend(repaint_rects)
            if self._repaint_all:
                self.window.repaint_areas.append(self.rect)
                self._repaint_all = False

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
                self.window.send_event_to_containers("setup", self)
            if hasattr(self, "on_setup") and callable(getattr(self, "on_setup")):
                self.window.send_event_to_containers("setup", self)
        self.window.run(self.image, full_screen=fullscreen)

    def switch_background(self, background: Union[int, Type[Appearance]]) -> background.Background:
        """Switches the background of costume

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: 
            The new costume

        """
        if type(background) == int:
            background = self.background.get_index(background)
        self.background = background
        self._repaint_all = 1
        [token.set_dirty() for token in self.tokens]
        return self.background

    def update(self):
        # This is the board-mainloop()
        # Called in miniworldwindow.update as ct.update()
        # Event handling is in miniworldwindow and is called before update().
        if self.is_running:
            # Acting for all actors
            if self.frame % self.speed == 0:
                self._act_all()
                self._handle_all_collisions()
            # run animations
            self._update_all_costumes()
            self._update_background()
            self._tick_timed_objects()
            # If there are physic objects, run a physics simulation step
            if physicsengine.PhysicsProperty.count > 0:
                physics_tokens = [token for token in self.tokens if token.physics and token.physics.started]
                physics.PhysicsProperty.simulation(physics_tokens)
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self._executed_events.clear()

    def _update_all_costumes(self):
        [token.costume.update() for token in self.tokens]

    def _update_background(self):
        if self.background:
            self.background.update()

    def _tick_timed_objects(self):
        [obj.tick() for obj in self.timed_objects]

    def handle_event(self, event, data=None):
        """
        Event handling

        Args:
            event (str): The event which was thrown, e.g. "key_up", "act", "reset", ...
            data: The data of the event (e.g. ["S","s"], (155,3), ...
        """
        # Call specific event handlers ("on_mouse_left", "on_mouse_right", ... for tokens
        if event not in self._executed_events:  # events shouldn't be called more than once per tick
            self._executed_events.add(event)
            from miniworldmaker.tokens import token
            token_classes = token.Token.all_subclasses()
            token_classes.add(token.Token)
            all_objects = list(self.tokens.sprites())
            all_objects.append(self)
            for a_object in all_objects:
                if event in ["reset"]:
                    self._handle_reset_event()
                if event in ["setup"]:
                    self._handle_setup_event()
                if event in ["switch_board"]:
                    self._handle_switch_board_event(*data)
                if event in ["key_down", "key_pressed", "key_down", "key_up"]:
                    self._handle_key_event(a_object, event, data)
                if event in ["mouse_left", "mouse_right", "mouse_motion"]:
                    self._handle_mouse_event(a_object, event, data)
                if event in ["clicked_left", "clicked_right"]:
                    self._handle_mouse_token_event(event, data)
                if event in ["message"]:
                    self._handle_message_event(a_object, event, data)
                if event in ["button_pressed"]:
                    self._handle_button_event(a_object, event, data)
            if event in self.registered_event_handlers.keys():
                # calls registered event handlers of board
                if data is None:
                    self.registered_event_handlers[event]()
                else:
                    try:
                        self.registered_event_handlers[event](self, data)
                    except TypeError:
                        raise TypeError("Wrong number of arguments for ", str(self.registered_event_handlers[event]),
                                        " with Arguments ", data)
            self.get_event(event, data)

    def _get_method(self, a_object, name):
        """
        If a (token-)object has method this returns the method by a given name
        """
        if hasattr(a_object, name):
            if callable(getattr(a_object, name)):
                _method = getattr(a_object, name)
                _bound_method = _method.__get__(a_object, a_object.__class__)
                return _bound_method
            else:
                return None
        else:
            return None

    def _call_method(self, receiver, method, args):
        try:
            sig = signature(method)
        except ValueError:
            raise Exception("Fehler beim aufrufen der registrierten Methode. Hast du die richtigen Argumente verwendet (auch 'self')?")
        # Don't call method if tokens are already removed:
        if issubclass(receiver.__class__, tkn.Token):
            if not receiver.board:
                return
        if args == None:
            method()
        elif len(sig.parameters) == len(args):
            method(*args)
        else:
            info = inspect.getframeinfo(inspect.currentframe())
            raise Exception(
                "Wrong number of arguments for " + str(method) + " in , got " + str(
                    len(args)) + " but should be " + str(
                    len(sig.parameters)) + "; "
                "File:" + str(info.filename), "; Method: " + str(method)
            )

    def _handle_key_event(self, receiver, event, data):
        # any key down?
        method = self._get_method(receiver, "on_" + str(event))
        if method:
            self._call_method(receiver, method, [data])
        # specific key down?
        for key in data:
            if key == key.lower():
                method = self._get_method(receiver, "on_" + event + "_" + key)
                if method:
                    self._call_method(receiver, method, None)

    def _handle_mouse_event(self, receiver, event, data):
        # any key down?
        method_name = "on_" + event
        method = self._get_method(receiver, method_name)
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_mouse_token_event(self, event, data):
        # any key down?
        token = data[0]
        position = data[1]
        method_name = "on_" + event
        method = self._get_method(token, method_name)
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)
        tokens = self.get_tokens_by_pixel(position)
        for token in tokens:
            method = self._get_method(token, method_name)
            if method:
                self._call_method(token, method, [position])

    def _handle_setup_event(self):
        if not self._is_setup:
            if hasattr(self, "setup") and callable(getattr(self, "setup")):
                self.setup()
                self._is_setup = True
            if hasattr(self, "on_setup") and callable(getattr(self, "on_setup")):
                self.on_setup()
                self._is_setup = True
        return self

    def _handle_reset_event(self):
        self.window.event_queue.clear()
        for token in self.tokens:
            token.remove()
        self.window.board = self.__class__(self.width, self.height)
        self.window.board.run()
        board = self.window.board
        board.event_queue.clear()
        del self
        return board

    def _handle_switch_board_event(self, old_board, Board, size: tuple):
        self.window.event_queue.clear()
        for token in self.tokens:
            token.remove()
        self.window.board = Board(size[0], size[1])
        board = self.window.board
        board.run()
        board.event_queue.clear()
        del self
        return board

    def _handle_act_event(self, receiver):
        # any key down?
        method = self._get_method(receiver, "act")
        if method:
            sig = signature(method)
            if len(sig.parameters) == 0:
                method()
            else:
                raise Exception("Wrong number of arguments for act-Method (should be: 0)")

    def _handle_button_event(self, receiver, event, data):
        # any key down?
        method = self._get_method(receiver, "on_button_pressed")
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_message_event(self, receiver, event, data):
        # any key down?
        method = self._get_method(receiver, "on_message")
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_all_collisions(self):
        for token in self.tokens:
            self._handle_collision_with_tokens(token)
            self._handle_collision_with_borders(token)
            self._handle_on_board(token)

    def _handle_collision_with_tokens(self, token):
        members = dir(token)
        found_tokens = []
        for token_type in [member[11:] for member in members if member.startswith("on_sensing_")]:
            tokens_for_token_type = token.sensing_tokens(token_type=token_type.capitalize())
            for found_token in tokens_for_token_type:
                if found_token not in found_tokens:
                    found_tokens.append(found_token)
        if found_tokens:
            for other_token in found_tokens:
                parents = inspect.getmro(other_token.__class__)
                other_and_parents = list(parents)
                if other_and_parents:
                    for other_class in other_and_parents:
                        method_name = ('on_sensing_' + str(other_class.__name__)).lower()
                        method = self._get_method(token, method_name)
                        if method:
                            self._call_method(token, method, [other_token])

    def _handle_collision_with_borders(self, token):
        border_methods_dict = {"on_sensing_left_border": self._get_method(token, "on_sensing_left_border"),
                               "on_sensing_right_border": self._get_method(token, "on_sensing_right_border"),
                               "on_sensing_bottom_border": self._get_method(token, "on_sensing_bottom_border"),
                               "on_sensing_top_border": self._get_method(token, "on_sensing_top_border"),
                               }
        on_sensing_borders = self._get_method(token, "on_sensing_borders")
        if on_sensing_borders or [method for method in border_methods_dict.values() if method is not None]:
            sensed_borders = token.sensing_borders()
            if sensed_borders:
                if on_sensing_borders:
                    self._call_method(token, on_sensing_borders, [sensed_borders])
                for key in border_methods_dict.keys():
                    if border_methods_dict[key]:
                        for border in sensed_borders:
                            if border in key:
                                self._call_method(token, border_methods_dict[key], None)

    def _handle_on_board(self, a_object):
        on_board_handler = self._get_method(a_object, 'on_sensing_on_board'.lower())
        not_on_board_handler = self._get_method(a_object, 'on_sensing_not_on_board'.lower())
        if on_board_handler or not_on_board_handler:
            is_on_board = a_object.sensing_on_board()
            if is_on_board:
                if on_board_handler:
                    on_board_handler()
            else:
                if not_on_board_handler:
                    not_on_board_handler()

    def save_to_db(self, file):
        """
        Saves the current board an all actors to database.
        The file is stored as db file and can be opened with sqlite.

        Args:
            file: The file as relative location

        Returns:

        """
        if os.path.exists(file):
            os.remove(file)
        db = db_manager.DBManager(file)
        query_actors = """     CREATE TABLE `token` (
                        `token_id`			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `column`		INTEGER,
                        `row`			INTEGER,
                        `token_class`	TEXT,
                        `parent_class`  TEXT
                        );
                        """
        query_board = """     CREATE TABLE `board` (
                        `tile_size`		INTEGER,
                        `rows`			INTEGER,
                        `columns`		INTEGER,
                        `tile_margin`	INTEGER,
                        `board_class`	TEXT
                        );
                        """
        cur = db.cursor
        cur.execute(query_actors)
        cur.execute(query_board)
        db.commit()
        for token in self.tokens:
            token_dict = {"column": token.position[0],
                          "row": token.position[1],
                          "token_class": token.__class__.__name__}
            db.insert(table="token", row=token_dict)
        board_dict = {"rows": self.rows,
                      "columns": self.columns,
                      "tile_margin": self.tile_margin,
                      "tile_size": self.tile_size,
                      "board_class": self.__class__.__name__}
        db.insert(table="board", row=board_dict)
        db.commit()
        db.close_connection()
        self.window.send_event_to_containers("Saved to db", file)

    def play_sound(self, path: str):
        if path.endswith("mp3"):
            path = path[:-4] + "wav"
        if path in self.sound_effects.keys():
            self.sound_effects[path].play()
        else:
            effect = self.register_sound(path)
            effect.play()

    def play_music(self, path: str):
        """
        plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background.count_pixels_by_color(rect, color, threshold)

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
        pos = board_position.BoardPosition.from_pixel(pygame.mouse.get_pos())
        clicked_container = self.window.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self:
            return pos
        else:
            return None

    def get_board_position_from_pixel(self, pixel):
        return board_position.BoardPosition.from_pixel(pixel)

    def _update_event_handling(self):
        self.tokens_with_eventhandler.clear()
        for token in self.tokens:
            for event_handler in self.registered_event_handlers_for_tokens[token.__class__].keys():
                self.tokens_with_eventhandler[event_handler].append(token)

    def is_position_on_board(self, position: board_position.BoardPosition) -> bool:
        """Tests if area or position is on board

        Args:
            position: A rectangle or a position

        Returns:
            True, if area is in grid

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

    def register_sound(self, path) -> pygame.mixer.Sound:
        """
        Registers a sound effect to board-sound effects library
        
        Args:
            path: The path to sound

        Returns: 
            the sound

        """
        try:
            effect = pygame.mixer.Sound(path)
            self.sound_effects[path] = effect
            return effect
        except pygame.error:
            raise FileExistsError("File '{0}' does not exist. Check your path to the sound.".format(path))

    @staticmethod
    def _get_token_class_by_name(name):
        return Board.token_classes.get(name, None)

    @staticmethod
    def _update_token_subclasses():
        """
        Returns a dict with class_name->class
        updat
        Returns:

        """
        token_subclasses = tkn.Token.all_subclasses()
        token_subclasses.add(tkn.Token)
        for cls in token_subclasses:
            Board.token_classes[cls.__name__] = cls
            if cls not in Board.token_class_ids:
                cls.class_id = Board.token_class_id_counter
                Board.token_class_ids[cls] = Board.token_class_id_counter
                Board.token_class_id_counter += 1
        return Board.token_classes

    def _register_physics_collision_handler(self, token):

        def add_physics_collision_handler(token, other_class, method):
            handler = physics.PhysicsProperty.space.add_collision_handler(token.__class__.class_id,
                                                                        other_class.class_id)
            handler.data["method"] = getattr(token, method)
            if method.startswith(Board.begin_prefix):
                handler.data["type"] = "begin"
                handler.begin = self._physics_collision_handler
            elif method.startswith(Board.separate_prefix):
                handler.data["type"] = "separate"
                handler.separate = self._physics_collision_handler

        Board._update_token_subclasses()
        method_list = [func for func in dir(token) if
                       (func.startswith(Board.begin_prefix) or func.startswith(Board.separate_prefix))
                       and
                       callable(getattr(token, func))]
        for method_name in method_list:
            if method_name.startswith(Board.begin_prefix):
                other_class_name = method_name[len(Board.begin_prefix):].capitalize()
            elif method_name.startswith(Board.separate_prefix):
                other_class_name = method_name[len(Board.separate_prefix):].capitalize()
            other_class = Board._get_token_class_by_name(other_class_name)
            if other_class is not None:
                child_classes = other_class.all_subclasses()
                for child_class in child_classes:
                    add_physics_collision_handler(token, child_class, method_name)
                add_physics_collision_handler(token, other_class, method_name)

    def _physics_collision_handler(self, arbiter, space, data):
        rvalue = None
        collision = dict()
        other_class = str(arbiter.shapes[1].token.__class__.__name__).lower()
        rvalue = self.pass_physics_collision_to_tokens(arbiter, space, data)
        if data["type"] == "begin":
            method = "on_touching_" + other_class
            method = self._get_method(arbiter.shapes[0].token, method)
            if method and callable(method):
                rvalue = method(arbiter.shapes[1].token, collision)
        if data["type"] == "separate":
            method = "on_separation_from_" + other_class
            method = self._get_method(arbiter.shapes[0].token, method)
            if method and callable(method):
                rvalue = method(arbiter.shapes[1].token, collision)
        if rvalue is None:
            return True
        else:
            return rvalue

    def pass_physics_collision_to_tokens(self, arbiter, space, data):
        collision = ()
        token = arbiter.shapes[0].token
        method_list = [func for func in dir(token.__class__) if
                       callable(getattr(token.__class__, func)) and (
                               func.startswith(Board.begin_prefix) or func.startswith(Board.separate_prefix))]
        for method_name in method_list:
            if method_name.startswith(Board.begin_prefix):
                registered_class_name = method_name[len(Board.begin_prefix):].capitalize()
            elif method_name.startswith(Board.separate_prefix):
                registered_class_name = method_name[len(Board.separate_prefix):].capitalize()
            registered_class = Board._get_token_class_by_name(registered_class_name)
            if registered_class is not None:
                child_classes_of_registered = registered_class.all_subclasses().union()
                if child_classes_of_registered is not None:
                    registered_classes = child_classes_of_registered.union({registered_class})
                else:
                    registered_classes = child_classes_of_registered = {registered_class}
                other = arbiter.shapes[1].token
                other_class = arbiter.shapes[1].token.__class__
                other_class_name = other_class.__name__.lower()
                if other_class in registered_classes:
                    if data["type"] == "begin":
                        method_name = str(Board.begin_prefix + registered_class_name).lower()
                    if data["type"] == "separate":
                        method_name = str(Board.separate_prefix + registered_class_name).lower()
                    method = self._get_method(token, method_name)
                    if method:
                        self._call_method(token, method, [other, collision])

    def add_event_handler_for_class(self, subcls, event, handler):
        handler = getattr(subcls, "on_" + event, None)
        if callable(handler):
            self.registered_event_handlers_for_tokens[subcls][event] = handler

    " @decorator"
    def register(self, method):
        bound_method = method.__get__(self, self.__class__)
        setattr(self, method.__name__, bound_method)
        return bound_method

    def send_message(self, message):
        self.window.send_event_to_containers("message", message)

    def screenshot(self, filename="screenshot.jpg"):
        pygame.image.save(self.surface,filename)

    def quit(self, exit_code = 0):
        self._app.quit(exit_code)