from __future__ import annotations

import inspect
from typing import List, Tuple, Union

import pygame

import miniworldmaker.appearances.background as background
import miniworldmaker.appearances.backgrounds_manager as backgrounds_manager
import miniworldmaker.base.app as app
import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.board_rect as board_rect
import miniworldmaker.boards.board_manager.board_collision_manager as coll_manager
import miniworldmaker.boards.board_manager.board_event_manager as event_manager
import miniworldmaker.boards.board_manager.board_mouse_manager as mouse_manager
import miniworldmaker.boards.data.export_factory as export_factory
import miniworldmaker.boards.data.import_factory as import_factory
import miniworldmaker.boards.token_connectors.token_connector as token_connector
import miniworldmaker.containers.container as container
import miniworldmaker.dialogs.ask as ask
import miniworldmaker.tokens.token as token_module
import miniworldmaker.tools.board_inspection as board_inspection
from miniworldmaker.exceptions.miniworldmaker_exception import (
    BoardArgumentsError,
    BoardInstanceError,
    NotImplementedOrRegisteredError,
)


class BaseBoard(container.Container):
    subclasses = None

    def __init__(
            self,
            columns: Union[int, Tuple[int]] = 400,
            rows: int = 400,
            tile_size: int = 1,
    ):
        if self.__class__ == BaseBoard:
            raise BoardInstanceError()
        if type(columns) != int or type(rows) != int:
            if type(columns) == tuple:
                size = columns
                columns = size[0]
                rows = size[1]
            else:
                raise BoardArgumentsError(columns, rows)
        self._columns, self._rows, self._tile_size = columns, rows, tile_size
        self._tokens = pygame.sprite.LayeredDirty()
        self.event_manager: event_manager.BoardEventHandler = event_manager.BoardEventHandler(self)
        super().__init__()
        self.backgrounds_manager: "backgrounds_manager.BackgroundsManager" = backgrounds_manager.BackgroundsManager(
            self
        )
        self.mouse_manager: "mouse_manager.BoardMouseManager" = mouse_manager.BoardMouseManager(self)
        self.ask: "ask.Ask" = ask.Ask(self)
        pygame.init()
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
        self.frame: int = 0
        self.clock: pygame.time.Clock = pygame.time.Clock()
        # Init graphics
        self.app: "app.App" = app.App("miniworldmaker")
        self.app.container_manager.add_container(self, "top_left")
        app.App.board = self
        self.background = background.Background(self)
        self.background.update()
        self.collision_manager: "coll_manager.BoardCollisionHandler" = coll_manager.BoardCollisionHandler(self)
        self.timed_objects: list = []
        self.app.event_manager.send_event_to_containers("setup", self)
        self.dynamic_tokens = set()
        self._registered_methods = []
        self.tokens_fixed_size = False
        self._container_width = self.columns * self.tile_size
        self._container_height = self.rows * self.tile_size

    def get_token_connector(self, token) -> token_connector.TokenConnector:
        return self._get_token_connector_class()(self, token)

    @staticmethod
    def _get_token_connector_class():
        return token_connector.TokenConnector

    def load_board_from_db(self, file: str):
        """
        Loads a sqlite db file.
        """
        return import_factory.ImportBoardFromDB(file, self.__class__).load()

    def load_tokens_from_db(self, file: str, token_classes: list) -> List["token_module.Token"]:
        """Loads all tokens from db. Usually you load the tokens in __init__() or in on_setup()

        Args:
            file (str): reference to db file
            token_classes (list): a list of all Token Classes which should be imported.

        Returns:
            [type]: All Tokens
        """
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
        export_factory.ExportTokensToDBFactory(file, self.tokens).save()

    def __str__(self):
        return "{0} with {1} columns and {2} rows".format(self.__class__.__name__, self.columns, self.rows)

    @property
    def container_width(self) -> int:
        """
        The width of the container
        """
        return self.columns * self.tile_size

    @property
    def container_height(self) -> int:
        """
        The height of the container
        """
        return self.rows * self.tile_size

    @property
    def has_background(self) -> bool:
        return self.backgrounds_manager.has_background

    @property
    def window(self) -> "app.App":
        """
        Gets the parent window

        Returns:
            The window

        """
        return self._window

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def registered_events(self) -> set:
        return self.event_manager.registered_events

    @registered_events.setter
    def registered_events(self, value):
        return  # setter is defined so that board_event_manager is not overwritten by board parent class container

    def remove_from_board(self, token: token_module.Token):
        """Removes a token from board.
        The method is called with token.remove()

        Args:
            token: The token to remove from board.

        """
        self.get_token_connector(token).remove_token_from_board(token)

    def add_to_board(self, token, position: tuple):
        """Adds a Token to the board.
        Is called in __init__-Method if position is set.

        Args:
            token: The token, which should be added to the board.
            position: The position on the board where the actor should be added.
        """
        self.get_token_connector(token).add_token_to_board(token, position)

    def blit_surface_to_window_surface(self):
        self.app.window.surface.blit(self.background.surface, self.rect)

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

    def remove_tokens_from_rect(self, rect, token_class=None, exclude=None):
        """Removes all tokens in an area

        Args:
            rect: A rectangle or a tuple (which is automated converted to a rectangle with tile_size).
            token_class: The class of the tokens which should be removed
            exclude: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area
        """
        rect = board_rect.Rect(self).create(rect)
        tokens = self.get_tokens_at_rect(rect)
        for token in tokens:
            if token is not None:
                [token.remove() for token in BaseBoard.filter_actor_list(tokens, token_class)]

    def repaint(self):
        self.background.repaint()  # called 1/frame in container.repaint()

    def update(self):
        # This is the board-mainloop()
        # Called in miniworldwindow.update as container.update()
        if self.is_running or self.frame == 0:
            # Acting for all actors
            if self.frame > 0 and self.frame % self.speed == 0:
                self.act_all()
                self._run_next_line_in_started_method()
            self.collision_manager.handle_all_collisions()
            self.mouse_manager.update_positions()
            # run animations
            self.background._update_all_costumes()
            self.background.update()
            self._tick_timed_objects()
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self.event_manager.executed_events.clear()

    def _run_next_line_in_started_method(self):
        for on_started_method in self.event_manager.registered_events["on_started"]:
            line_number = self.frame // self.speed + 1
            if on_started_method and self.frame % self.speed == 0 and self.frame != 0:
                self._run_line(on_started_method, line_number)

    @staticmethod
    def _run_line(method: callable, line_number: int):
        method_source = inspect.getsourcelines(method)[0]
        if line_number < len(method_source):
            exec(method_source[line_number].strip())

    def act_all(self):
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

    def _update_event_handling(self):
        self.event_manager.update_event_handling()

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
        
    def add_container(self, container, dock, size=None):
        return self.app.container_manager.add_container(container, dock, size)

    def get_tokens_by_class_name(self, classname: str):
        return [token for token in self._tokens if token.__class__.__name__ == classname]

    def get_tokens_by_class(self, classname: str):
        return [token for token in self._tokens if isinstance(token, classname)]

    def on_started(self):
        """The on_started method is executed after starting the board.
        Afterwards the individual lines are executed step by step with some delay (depending on board.speed).

        Examples:

        Registering an on_started-Method

        .. code-block:: python

            @karaboard.register
            def on_started(self):
                self.kara.move_right()
                self.kara.move_right()


        Raises:
            NotImplementedOrRegisteredError: The error is raised when method is not overwritten or registered.
        """
        raise NotImplementedOrRegisteredError()

    def borders(self, value: Union[tuple, "board_position.Position", pygame.Rect]) -> list:
        """
        Gets all borders a rect is touching

        Args:
            rect: The rect

        Returns: A list of borders, e.g. ["left", "top", if rect is touching the left a top border.

        """
        pass

    def is_on_board(self) -> bool:
        self.is_position_on_board(self.position)

    def _filter_tokens_by_type(self, token_list, token_type):
        filtered_tokens = token_list
        # token class_name --> class
        if type(token_type) == str:  # is token_type a string
            token_type = self.find_token_class_for_name(token_type)
        # single token --> list
        if isinstance(token_type, token_module.Token):  # is_token_type an object?
            token_list = [token_type]
        # filter
        if token_type:
            filtered_tokens = [
                token
                for token in token_list
                if (issubclass(token.__class__, token_type) or token.__class__ == token_type)
            ]
        return filtered_tokens

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
        self.app.window.dirty = 1
        self.background.reload_transformations_after("all")
