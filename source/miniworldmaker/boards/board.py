import logging
from typing import Union
import os
import pygame
from containers import container
from windows import miniworldwindow as window
from tools import db_manager
from tokens import token
from boards import board_position
from boards import background
from boards import area
from math import hypot

class Board(container.Container):
    """
    Base class for creating boards
    """
    log = logging.getLogger("GameGrid")
    registered_token_types = {}
    lookup = True

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 ):
        """Creates a new board

        Args:
            columns: columns of new board
            rows: rows of new board
        """
        super().__init__(self)
        pygame.init()
        # public
        self.active_token = None
        self.register_events = {"mouse_left", "mouse_right", "key_pressed", "key_pressed", "key_down"}
        self.is_running = True
        self.steps = 1
        # private
        self._speed = 60
        self._tokens = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._key = 0
        self._animated = False
        self._grid = []
        self._tile_size = 1
        self._tile_margin = 0
        self._columns, self._rows = columns, rows
        self.set_size(self.tile_size, columns, rows, self.tile_margin)
        self.background = background.Background(self)
        self._image = self.background.image
        self._max_diameter = self._tile_size
        # protected
        self.dirty = 1
        self.frame = 0
        self._tick = 0
        self.clock = pygame.time.Clock()
        self.__last_update = pygame.time.get_ticks()
        # Init graphics
        self.dirty = 1
        self._window = window.MiniWorldWindow("MiniWorldMaker")
        self._window.add_container(self, "main")
        window.MiniWorldWindow.board = self

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value
        self.window.send_event_to_containers("board_speed_changed", self._speed)

    def set_size(self,
                 tile_size: int = 1,
                 columns: int = 40,
                 rows: int = 40,
                 tile_margin: int = 0):
        """Sets size of a board

        Args:
            tile_size: Size of a tile in pixels
            columns: Number of columns
            rows: Number of rows
            tile_margin: margin bewtween tiles

        """
        self._tile_size = tile_size
        self._columns = columns
        self._rows = rows
        self._tile_margin = tile_margin
        self._grid = []
        self.log.info("Set Board Size to {0} columns and {1} rows".format(self.columns, self.rows))
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)
        self.dirty = 1

    def __str__(self):
        return "{0} with {1} columns and {2} rows".format(self.__class__.__name__, self.columns, self.rows)

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(actor) == actor_type]

    def get_event(self, event, data):
        """Event handling. Overwrite in your subclass

        Args:
            event: The event (e.g. mouse_left, ...)
            data: The data associated with the event
        """
        pass

    @property
    def width(self) -> int:
        if self.dirty == 0:
            return self._container_width
        else:
            self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
            return self._container_width

    @property
    def height(self) -> int:
        if self.dirty == 0:
            return self._container_height
        else:
            self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
            return self._container_height

    @property
    def window(self) -> window.MiniWorldWindow:
        return self._window

    @property
    def tile_size(self):
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value: int):
        """ Sets the tile-size"""
        self._tile_size = value

    @property
    def tile_margin(self) -> int:
        return self._tile_margin

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.dirty = 1

    @property
    def columns(self) -> int:
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.dirty = 1

    @property
    def tokens(self):
        return self._tokens

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def add_image(self, path: str) -> int:
        """Adds image to current costume

        Args:
            path: The path to the image as relative path

        Returns:
            The index of the image.

        """
        return self.background.add_image(path)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._image = self.background.image
            return self.background.image

    def add_to_board(self, token: token.Token, position: Union[tuple, board_position.BoardPosition]) -> token.Token:
        """Adds token to board

        Args:
            token: The token which should be added
            position: The position the token should be added

        Returns:
            The Token

        """
        self.tokens.add(token)
        if type(position) == tuple:
            token.position = board_position.BoardPosition(position[0], position[1])
        elif type(position) == board_position.BoardPosition:
            token.position = position
        else:
            raise AttributeError("Position has wrong type" + str(type(position)))
        token.add_to_board(self, position)
        self._max_diameter = max(hypot(*token.rect.size) for token in self.tokens)
        self.window.send_event_to_containers("Added token", token)
        return token

    def get_token_by_pixel(self, pixel: tuple) -> list:
        """Gets all tokens by Pixel.

        This method can be used, if you want to get a token by mouse-clock

        Args:
            pixel: the pixel-coordinates

        Returns:
            A list of tokens

        """
        actors = []
        for actor in self.tokens:
            if actor.rect.collidepoint(pixel):
                actors.append(actor)
        return actors

    def get_tokens_in_area(self, area: Union[pygame.Rect, tuple], token=None, exclude=None) -> list:
        """Gets all tokens in area

        Args:
            area: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be added
            exclude: A token which should not be returned e.g. the actor itself

        Returns:
            all tokens in the area as list

        """
        tokens = []
        if type(area) == tuple:
            area = pygame.Rect(area[0], area[1], self.tile_size, self.tile_size)
        if token is not None:
            token_list = self.filter_actor_list(self.tokens, token)
            token_list.remove(exclude)
        else:
            token_list = self.tokens
        for token in token_list:
            if token.rect.colliderect(area):
                tokens.append(token)
        return tokens

    def get_token_in_area(self, value: Union[pygame.Rect, tuple], token=None, exclude=None) -> token.Token:
        """Gets  a single tokens in area

        Args:
            value: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be added
            excluded: A token which should not be returned e.g. the actor itself

        Returns:
            One token

        """
        if type(value) == tuple:
            value = pygame.Rect(value[0], value[1], 1, 1)
        if token is not None:
            token_list = self.filter_actor_list(self.tokens, token)
        else:
            token_list = self.tokens
        if exclude in token_list:
            token_list.remove(exclude)
        for token in token_list:
            if token.rect.colliderect(value):
                return token

    def remove_actors_from_area(self, area: Union[tuple, pygame.Rect], token=None, exclude=None):
        """Removes all tokens in an area

        Args:
            area: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be removed
            excluded: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area

        """
        if type(area) == tuple:
            area = pygame.Rect(area[0], area[1], 1, 1)
        tokens = self.get_tokens_in_area(area)
        if token is not None:
            tokens = self.filter_actor_list(tokens, token)
        for actor in tokens:
            self.remove_from_board(actor)

    def remove_from_board(self, token: token.Token):
        """Removes a single token from board

        Args:
            token: The token which should be removed

        """
        if token:
            self.tokens.remove(token)
            token.board = None

    def is_on_board(self, area: Union[board_position.BoardPosition, pygame.Rect]) -> bool:
        if type(area) == tuple:
            area = board_position.BoardPosition(area[0], area[1])
        if type(area) == board_position.BoardPosition:
            area = area.to_rect()

        top_left_x, top_left_y, right, top = area.topleft[0], \
                                             area.topleft[1], \
                                             area.right, \
                                             area.top
        if top_left_x < 0 or top_left_y < 0 or area.right >= self.width or area.bottom >= self.height:
            return False
        else:
            return True

    def borders(self, actor):
        pass

    def repaint(self):
        self._window.repaint_areas.extend(self.tokens.draw(self.image))
        if self.dirty == 1:
            self._window.repaint_areas.append(self.rect)
            self.dirty = 0

    def show(self):
        """
        Starts the program

        """
        self.tokens.clear(self.image, self.image)
        self.dirty = 1
        logging.basicConfig(level=logging.WARNING)
        self._max_diameter = max(hypot(*token.rect.size) for token in self.tokens)
        self.window.show()

    def update(self):
        if self.is_running:
            self._act_all()
        self.frame = self.frame + 1
        for token in self.tokens:
            token.update()
        self.clock.tick(40)

    def _act_all(self):
        self._tick = self._tick + 1
        if self._tick > 101 - self.speed:
            tokens = [token for token in self.tokens if token.is_static == False]
            for token in tokens:
                token.act()
            self.act()
            self._tick = 0

    def pass_event(self, event, data=None):
        if event == "collision":
            for actor in self.tokens:
                if data[0] == actor:
                    actor.get_event("collision", data[1])
                elif data[1] == actor:
                    actor.get_event("collision", data[0])
        elif event == "mouse_left":
            if self.get_token_by_pixel(data):
                self.set_active_token(self.get_token_by_pixel(data)[0])
        else:
            for actor in self.tokens:
                actor.get_event(event, data)
            pass

    def set_active_token(self, token: token.Token):
        self.active_token = token
        token.dirty = 1
        self.window.send_event_to_containers("active_token", token)
        return token

    def act(self):
        """Custom acting

        This method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def show_log(self):
        logging.basicConfig(level=logging.INFO)

    def save_to_db(self, file):
        os.remove(file)
        db = db_manager.DBManager(file)
        self.log.info("Create db...")
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
        self.log.info("Save to db...")
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

    @classmethod
    def from_db(cls, file):
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
                if token_class_name in Board.registered_token_types.keys():
                    token_instance = Board.registered_token_types[token_class_name]()
                    board.add_to_board(token=token_instance, position=(tokens[1], tokens[2]))
        board.window.send_event_to_containers("Loaded from db", board)
        return board

    @staticmethod
    def register_token_type(class_name):
        Board.registered_token_types[class_name.__name__] = class_name

    def play_sound(self, sound_path):
        effect = pygame.mixer.Sound(sound_path)
        effect.play()

    def play_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def get_pixel_from_board_position(self, pos: board_position.BoardPosition) -> pygame.Rect:
        rect = pos.to_rect()
        return rect.topleft

    def get_board_position_from_pixel(self, position: tuple) -> tuple:
        column = (position[0] - self.tile_margin) // (self.tile_size + self.tile_margin)
        row = (position[1] - self.tile_margin) // (self.tile_size + self.tile_margin)
        return column, row

    def get_board_position_from_rect(self, position: pygame.Rect) -> tuple:
        position = position.topleft
        return self.get_board_position_from_pixel(position)

    def get_color_at_board_position(self, position: Union[tuple, board_position.BoardPosition]) -> list:
        if type(position == tuple):
            position = board_position.BoardPosition(position[1], position[0])
        self.dirty = 1
        return self.background._renderer.color_at(self.get_pixel_from_board_position(pos=position))

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background._renderer.color_at_rect(rect, color, threshold)
