from typing import Union
import os
import sys
import pygame
import math
from miniworldmaker.containers import container
from miniworldmaker.windows import miniworldwindow as window
from miniworldmaker.tools import db_manager
from miniworldmaker.tokens import token as pck_token
from miniworldmaker.boards import board_position
from miniworldmaker.boards import background
from miniworldmaker.physics import physics as physicsengine
from collections import defaultdict
import types


class Board(container.Container):
    """
    Base class for creating boards
    """
    registered_token_types = {}

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 ):
        """Creates a new board

        Args:
            columns: columns of new board
            rows: rows of new board
        """
        super().__init__()
        pygame.init()
        # public
        self.active_actor = None
        self.register_events = {"all"}
        self.is_running = True
        self.default_actor_speed = 1 #: default speed for actors
        self.sound_effects = {}
        # private
        self._world_speed = 100
        self._tokens = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._key = 0
        self._animated = False
        self._grid = []
        self._tile_size = 1
        self._tile_margin = 0
        self._repaint_all = 0
        self._columns, self._rows = columns, rows
        self.set_size(self.tile_size, columns, rows, self.tile_margin)
        self.background = background.Background(self)
        self.backgrounds = [self.background]
        self._image = pygame.Surface((1, 1))
        self.surface = pygame.Surface((1, 1))
        # protected
        self.frame = 0
        self._tick = 0
        self.clock = pygame.time.Clock()
        self.clock = pygame.time.Clock()
        self.__last_update = pygame.time.get_ticks()
        # Init graphics
        self.dirty = 1
        self._window = window.MiniWorldWindow("MiniWorldMaker")
        self._window.add_container(self, "top_left")
        window.MiniWorldWindow.board = self
        self.shapes_fill_color = (0, 0, 0, 0)
        self.registered_event_handlers = defaultdict(list)

    def fill(self, color):
        self.shapes_fill_color = color


    @property
    def speed(self) -> int:
        return self._world_speed

    @speed.setter
    def speed(self, value: int):
        self._world_speed = value
        self.window.send_event_to_containers("board_speed_changed", self._world_speed)

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
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)
        self.dirty = 1
        self._repaint_all = 1

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

    def get_tile_rect(self):
        return pygame.Rect(0, 0, self.tile_size, self.tile_size)

    @property
    def container_width(self):
        self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
        return self._container_width

    @property
    def width(self) -> int:
        """
        The width of the board in tiles (or pixels if board is pixel-board
        """
        if self.dirty == 0:
            return self._container_width
        else:
            return self.container_width

    @property
    def container_height(self):
        self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
        return self._container_height

    @property
    def height(self) -> int:
        """
        The height of the board in tiles (or pixels if board is pixel-board
        """
        if self.dirty == 0:
            return self._container_height
        else:
            return self.container_height

    @property
    def window(self) -> window.MiniWorldWindow:
        """
        The window
        Returns: The window

        """
        return self._window

    @property
    def tile_size(self) -> int:
        """
        The size of the tiles
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value: int):
        """ Sets the tile-size"""
        self._tile_size = value

    @property
    def tile_margin(self) -> int:
        """
        The margin between tiles
        """
        return self._tile_margin

    @property
    def rows(self) -> int:
        """
        The number of rows
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.dirty = 1
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
        self.dirty = 1
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

    def add_image(self, path: str) -> int:
        """Adds image to current costume

        Args:
            path: The path to the image as relative path

        Returns:
            The index of the image.

        """
        try:
            image = self.background.add_image(path)
        except FileExistsError:
            raise FileExistsError("File '{0}' does not exist. Check your path to the image.".format(path))
        return image

    def add_background(self, path: str) -> background.Background:
        new_background = background.Background(self)
        new_background.add_image(path)
        new_background.orientation = self.background.orientation
        self.backgrounds.append(new_background)
        return new_background

    def switch_background(self, index=-1) -> background.Background:
        """Switches costume

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: The new costume

        """
        if index == -1:
            index = self.backgrounds.index(self.background)
            if index < len(self.backgrounds) - 1:
                index += 1
            else:
                index = 0
        else:
            index = index
        self.background = self.backgrounds[index]
        self.background.dirty = 1
        self.background.changed_all()
        self.dirty = 1
        self._repaint_all = 1
        for token in self.tokens:
            token.dirty = 1
        return self.background

    def add_to_board(self, token: pck_token.Token, position: Union[tuple, board_position.BoardPosition]) -> pck_token.Token:
        """Adds token to board

        Args:
            token: The token which should be added
            position: The position the token should be added

        Returns:
            The Token

        """
        self.tokens.add(token)
        if type(position) == tuple:
            token.position = board_position.BoardPosition(position)
        elif type(position) == board_position.BoardPosition:
            token.position = position
        else:
            raise AttributeError("Position has wrong type" + str(type(position)))
        if token.speed == 0:
            token.speed = self.default_actor_speed
        token.add_to_board(self, position)
        self.window.send_event_to_containers("Added token", token)
        return token

    def reset(self):
        """Resets the board
        Creates a new board with init-function - recreates all tokens and actors on the board.

        Returns:
            The newly created and reseted board
        """
        board = self.__class__()
        board.is_running = False
        board.window.send_event_to_containers("reset", board)
        board.show()
        return board

    def get_tokens_by_pixel(self, pixel: tuple) -> list:
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
            if exclude in token_list:
                token_list.remove(exclude)
        else:
            token_list = self.tokens
        for token in token_list:
            if token.rect.colliderect(area):
                tokens.append(token)
        return tokens

    def get_token(self, value: Union[pygame.Rect, tuple], token=None, exclude=None) -> pck_token.Token:
        """Gets  a single tokens in area

        Args:
            value: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be added
            exclude: A token which should not be returned e.g. the actor itself

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
            exclude: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area

        """
        if type(area) == tuple:
            area = pygame.Rect(area[0], area[1], 1, 1)
        tokens = self.get_tokens_in_area(area)
        if token is not None:
            tokens = self.filter_actor_list(tokens, token)
        for actor in tokens:
            self.remove_from_board(actor)

    def remove_from_board(self, token: pck_token.Token):
        """Removes a single token from board

        Args:
            token: The token which should be removed

        """
        if token:
            self.tokens.remove(token)
            token.board = None

    def is_on_board(self, area: Union[board_position.BoardPosition, pygame.Rect]) -> bool:
        """Tests if area or position is on board
        Args:
            area: A rectangle or a position

        Returns: true, if area is in grid

        """
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

    @property
    def image(self) -> pygame.Surface:
        """
        The current displayed image
        """
        if not self.dirty:
            return self._image
        else:
            self._image = self.background.image
            return self._image

    def repaint(self):
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
        if self.dirty:
            self.surface.blit(self.image, self.surface.get_rect())
        self.tokens.clear(self.surface, self.image)
        repaint_rects = self.tokens.draw(self.surface)
        self._window.repaint_areas.extend(repaint_rects)
        if self._repaint_all == 1:
            self._window.repaint_areas.append(self.rect)
            self._repaint_all = 0

    def blit_surface_to_window_surface(self):
        if self.dirty:
            self._window.window_surface.blit(self.surface, self.rect)

    def show(self, fullscreen=False):
        """
        Starts the program.
        """
        self.background.is_scaled = True
        size = self.width, self.height
        self.background.size = (size)
        image = self.image
        self.window.show(image, full_screen= fullscreen)

    def run(self):
        pass

    def update(self):
        if self.is_running:
            self._tick = self._tick + 1
            if self._tick > 101 - self.speed:
                self._act_all()
                self._tick = 0
            for token in self.tokens:
                if token.physics:
                    token.physics.update_physics_model()
            steps = 1
            for x in range(steps):
                if physicsengine is not None and \
                        physicsengine.PhysicsProperty.space is not None:
                    physicsengine.PhysicsProperty.space.step(1 / 60)
            for token in self.tokens:
                if token.physics:
                    token.physics.update_token_from_physics_model()

        self.frame = self.frame + 1
        self.clock.tick(40)

    def _act_all(self):
        tokens = [token for token in self.tokens if token.is_static == False]
        for token in tokens:
            token.act()
        self.act()

    def pass_event(self, event, data=None):
        tokens = [token for token in self.tokens if token.is_static is False]
        if event == "mouse_left":
            tokens = self.get_tokens_by_pixel(data)
            if tokens:
                i = 0
                while i < len(tokens):
                    if self.active_actor == tokens[i]:
                        if i < len(tokens)-1:
                            self.set_active_actor(tokens[i+1])
                            break
                        else:
                            self.set_active_actor(tokens[0])
                            break
                    i = i + 1
                else:
                    self.set_active_actor(tokens[0])
        else:
            for token in tokens:
                if data != token:
                    token.get_event(event, data)
        if event in self.registered_event_handlers.keys():
            lst = self.registered_event_handlers[event]
            for handler in lst:
                handler(event, data)

    def register_act_method(self, method):
        self.method = types.MethodType(method, self)

    def set_active_actor(self, token: pck_token.Token):
        self.active_actor = token
        token.dirty = 1
        self.window.send_event_to_containers("active_token", token)
        help(token)
        return token

    def act(self):
        """Custom acting

        This method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def save_to_db(self, file):
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
                token_class = pck_token.Token
                class_list = Board.all_subclasses(pck_token.Token)

                for cls_obj in class_list:
                    if cls_obj.__name__ == token_class_name:
                        token_class = cls_obj
                token_class(position=(tokens[1], tokens[2])) # Create token
        board.window.send_event_to_containers("Loaded from db", board)
        return board

    @classmethod
    def all_subclasses(self, cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in self.all_subclasses(c)])

    @staticmethod
    def register_token_type(class_name):
        Board.registered_token_types[class_name.__name__] = class_name

    def play_sound(self, path: str):
        if path.endswith("mp3"):
            path = path[:-4] + "wav"
        if path in self.sound_effects.keys():
            self.sound_effects[path].play()
        else:
            effect = self.register_sound(path)
            effect.play()

    def register_sound(self, path) -> pygame.mixer.Sound:
        """
        Registers a sound effect to board-sound effects library
        Args:
            path: The path to sound

        Returns: the sound

        """
        effect = pygame.mixer.Sound(path)
        self.sound_effects[path] = effect
        return effect

    def play_music(self, path : str):
        """
        plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def get_board_position_from_pixel(self, position: tuple) -> board_position.BoardPosition:
        column = (position[0] - self.tile_margin) // (self.tile_size + self.tile_margin)
        row = (position[1] - self.tile_margin) // (self.tile_size + self.tile_margin)
        return board_position.BoardPosition((column, row))

    def get_board_position_from_rect(self, position: pygame.Rect) -> board_position.BoardPosition:
        position = position.topleft
        return self.get_board_position_from_pixel(position)

    def get_color_at_board_position(self, position: Union[tuple, board_position.BoardPosition]) -> tuple:
        if type(position == tuple):
            position = board_position.BoardPosition(position)
        return self.background.color_at(position.to_pixel())

    def get_colors_at_line(self, line: list):
        colors = []
        for pos in line:
            color_at_pos = self.background.color_at(pos)
            if color_at_pos not in colors:
                colors.append(color_at_pos)
        return colors

    def get_color_at_rect(self, rect : pygame.Rect, directions = None) -> list:
        colors = []
        for x in range(rect.width):
            if directions is None or "left" in directions:
                color = self.background.color_at((rect.x+x, rect.y))
                if color not in colors:
                    colors.append(color)
            if directions is None or "right" in directions:
                color = self.background.color_at((rect.x+x, rect.y+rect.height))
                if color not in colors:
                    colors.append(color)
        for y in range(rect.height):
            if directions is None or "top" in directions:
                color = self.background.color_at((rect.x, rect.y+y))
                if color not in colors:
                   colors.append(color)
            if directions is None or "bottom" in directions:
                color = self.background.color_at((rect.x+rect.width, rect.y+y))
                if color not in colors:
                    colors.append(color)
        return colors

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background.count_pixels_by_color(rect, color, threshold)

    def get_mouse_position(self):
        pos = pygame.mouse.get_pos()
        clicked_container = self.window.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self:
            return pos
        else:
            return None