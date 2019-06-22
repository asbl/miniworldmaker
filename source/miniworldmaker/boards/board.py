import os
from typing import Union

import pygame
from miniworldmaker.boards import background
from miniworldmaker.boards import board_position
from miniworldmaker.containers import container
from miniworldmaker.physics import physics as physicsengine
from miniworldmaker.tokens import token as pck_token
from miniworldmaker.tools import db_manager
from miniworldmaker.windows import miniworldwindow as window


class Board(container.Container):
    """Base Class for Boards

    Args:
        columns: columns of new board (default: 40)
        rows: rows of new board (default:40)

    """
    registered_token_types = {}

    def __init__(self,
                 columns: int = 40,
                 rows: int = 40,
                 ):

        super().__init__()
        pygame.init()
        # public
        self.active_actor = None
        self.register_events = {"all"}
        self.is_running = True
        self.default_actor_speed = 1 #: default speed for actors
        self.sound_effects = {}
        # private
        self._world_speed = 10  # property speed
        self._tokens = pygame.sprite.LayeredDirty()
        self.actors = None
        self._key_pressed = False
        self._animated = False
        self._grid = []
        self._tile_size, self._tile_margin = 1, 0
        self._repaint_all = False
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
        self.dirty = 1 # Information: A board is always dirty
        self._window = window.MiniWorldWindow("MiniWorldMaker")
        self._window.add_container(self, "top_left")
        window.MiniWorldWindow.board = self
        self.registered_event_handlers = dict()
        self.registered_event_handlers["mouse_left"] = self.on_mouse_left
        self.registered_event_handlers["mouse_right"] = self.on_mouse_left
        self.registered_event_handlers["mouse_motion"] = self.on_mouse_motion
        self.registered_event_handlers["key_pressed"] = self.on_key_pressed
        self.registered_event_handlers["key_down"] = self.on_key_down
        self.registered_event_handlers["key_up"] = self.on_key_up
        self.registered_event_handlers["board_created"] = self.on_setup
        self.window.send_event_to_containers("board_created", None)

    def update_actors(self):
        import miniworldmaker.tokens.actor as act
        self.actors = [token for token in self.tokens if issubclass(token.__class__, act.Actor)]


    def on_key_pressed(self, keys):
        """
        This method is called by a key_pressed_event.
        If you hold down the key, the event is triggered again and again until you release the key.
        The method should be overwritten in your custom Board-Class

        Args:
            keys: A list of keys

        Examples:
            Reaction to a key event:

            >>> def on_key_pressed(self, keys):
            >>>     if "W" in keys:
            >>>         pass

        """
        pass

    def act(self):
        """
        The act() - Method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def on_key_up(self, keys):
        """
        This method is called by a key_up event.
        The method should be overwritten in your custom Board-Class

        Args:
            keys: A list of keys

        Examples:
            Reaction to a key event:

            >>> def on_key_up(self, keys):
            >>>     if "W" in keys:
            >>>         pass

        """
        pass

    def on_key_down(self, keys):
        """
        This method is called by a key_down event.
        The method should be overwritten in your custom Board-Class

        Args:
            keys: A list of keys

        Examples:
            Reaction to a key event:

            >>> def on_key_up(self, keys):
            >>>     if "W" in keys:
            >>>         pass

        """
        pass

    def get_event(self, event, data):
        """
        The method is triggered by all types of events.

        Args:
            event: The event (e.g. mouse_left, ...)
            data: The data associated with the event

        Examples:
            Reaction to a key event:

            >>> def get_event(self, event, data):
            >>>     if event="key_down":
            >>>         if "W" in data:
            >>>             pass
        """
        pass

    def on_mouse_left(self, mouse_pos):
        """
        The method is triggered by mouse_left button.

        Args:
            mouse_pos: The mouse position as BoardPosition (x,y)

        Examples:
            Reaction to a mouse_left event

            >>> def on_mouse_left(self, mouse_pos):
            >>>     an_actor.point_towards_position(mouse_pos)
        """
        pass

    def on_mouse_right(self, mouse_pos):
        """
         The method is triggered by mouse_right button.

         Args:
             mouse_pos: The mouse position as BoardPosition (x,y)

         Examples:
             Reaction to a mouse_right event

             >>> def on_mouse_right(self, mouse_pos):
             >>>     an_actor.point_towards_position(mouse_pos)
         """
        pass

    def on_mouse_motion(self, mouse_pos):
        """
         The method is triggered by mouse_motion button.

         Args:
             mouse_pos: The mouse position as BoardPosition (x,y)

         Examples:
             Reaction to a mouse_motion event

             >>> def on_mouse_motion(self, mouse_pos):
             >>>     an_actor.point_towards_position(mouse_pos)
         """
        pass

    def on_setup(self):
        """
           The method is called with __init__ when creating a new board.

        """
        pass

    def fill(self, color):
        """
        Fills the background with a color

        Args:
            color: The color as 4-tuple (r, g, b, alpha
        """
        self.background.fill(color)

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

    def get_tile_rect(self):
        return pygame.Rect(0, 0, self.tile_size, self.tile_size)

    @property
    def container_width(self) -> int:
        """
        Gets the width of the container

        Returns:
            The width of the container (in pixels on a PixelGrid; in Tiles on a TiledGrid)

        """
        if self.dirty:
            self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
        return self._container_width

    @property
    def width(self) -> int:
        """
        See container_width
        """
        return self.container_width

    @property
    def container_height(self) -> int:
        """
        Gets the height of the container

        Returns:
            The height of the container (in pixels on a PixelGrid; in Tiles on a TiledGrid)

        """
        if self.dirty:
            self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
        return self._container_height

    @property
    def height(self) -> int:
        """
        See container_height
        """
        return self.container_height

    @property
    def window(self) -> window.MiniWorldWindow:
        """
        Gets the parent window

        Returns:
            The window

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
        """
        Adds image to current background.
        If no background is created yet, a new background will be created with this image.

        Args:
            path: The path to the image as relative path

        Returns:
            The index of the image.

        Examples:
            >>> class MyBoard(Board):
            >>>     def __init__(self):
            >>>         super().__init__(columns=400, rows=200)
            >>>         self.add_image(path="images/stone.jpg")
            Creates Board with file stone.jpg in folder images as background

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
        self.background_changed = 1
        self._repaint_all = True
        for token in self.tokens:
            token.dirty = 1
        return self.background

    def add_to_board(self, token: pck_token.Token, position: Union[tuple, board_position.BoardPosition]) -> pck_token.Token:
        """Adds token to board.

        Usually this method musn't be called.
        If you create a token with position-parameter, the token will be automaticly added to the board.

        Args:
            token: The token which should be added
            position: The position the token should be added

        Returns:
            The Token

        Examples:

            This code:

            >>> Robot(position=(50, 50))

            Does the same as:

            >>> robot = Robot()
            >>> self.add_to_board(Robot, position=(50, 50))
        """
        self.tokens.add(token)
        if type(position) == tuple:
            token.position = board_position.BoardPosition(position[0], position[1])
        elif type(position) == board_position.BoardPosition:
            token.position = position
        else:
            raise AttributeError("Position has wrong type" + str(type(position)))
        if token.speed == 0:
            token.speed = self.default_actor_speed
        token.add_to_board(self, position)
        self.update_actors()
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

        This method can be used, if you want to get a token by mouse-click

        Args:
            pixel: the pixel-coordinates

        Returns:
            A list of tokens

        """
        token = []
        for actor in self.tokens:
            if actor.rect.collidepoint(pixel):
                token.append(actor)
        return token

    def get_tokens_at_position(self, position, token_type=None, exclude=None) -> list:
        pass

    def get_tokens_in_area(self, area: pygame.Rect, singleitem=False, exclude=None, token_type = None):
        """Gets all tokens in area

        Args:
            area: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be added
            exclude: A token which should not be returned e.g. the actor itself

        Returns:
            all tokens in the area as list

        """
        tokens = []
        token_list = self.tokens.copy()
        if exclude in token_list:
            token_list.remove(exclude)
        if token_type is not None:
            tokens = [token for token in token_list if type(token) == token_type]
        for token in token_list:
            if token.rect.colliderect(area):
                tokens.append(token)
                if singleitem:
                    return token
        return tokens

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
            self.update_actors()

    @property
    def image(self) -> pygame.Surface:
        """
        The current displayed image
        """
        self._image = self.background.image
        return self._image

    def repaint(self):
        if self._repaint_all:
            self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            self.surface.blit(self.image, self.surface.get_rect())
        self.tokens.clear(self.surface, self.image)
        repaint_rects = self.tokens.draw(self.surface)
        self._window.repaint_areas.extend(repaint_rects)
        if self._repaint_all:
            self._window.repaint_areas.append(self.rect)
            self._repaint_all = False

    def blit_surface_to_window_surface(self):
        self._window.window_surface.blit(self.surface, self.rect)

    def show(self, fullscreen=False):
        """
        The method show() should always called at the end of your program.
        It starts the mainloop.

        Examples:
            >>> my_board = Board() # or a subclass of Board
            >>> my_board.show()

        """
        self.background.is_scaled = True
        self.background.size = self.container_width, self.container_height
        image = self.image
        self.window.show(image, full_screen= fullscreen)

    def update(self):
        if self.is_running:
            self._tick = self._tick + 1
            if self._tick == self.speed:
                self._tick = 0
                self._act_all()
                if physicsengine.PhysicsProperty.count > 0:
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
        if self.actors:
            for actor in self.actors:
                actor.act()
        self.act()

    def pass_event(self, event, data=None):
        if event == "mouse_left":
            # Test an token was clicked and set the active token
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
            # calls all registered event handlers of tokens
            if self.actors:
                for actor in [actor for actor in self.actors if event in actor.registered_event_handlers.keys()]:
                    actor.get_event(event, data)
                    actor.registered_event_handlers[event](data)
        if event in self.registered_event_handlers.keys():
            # calls registered event handlers of board
            if data is None:
                self.registered_event_handlers[event]()
            else:
                self.registered_event_handlers[event](data)

    def set_active_actor(self, token: pck_token.Token):
        self.active_actor = token
        token.dirty = 1
        self.window.send_event_to_containers("active_token", token)
        help(token)
        return token

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

    @classmethod
    def from_db(cls, file):
        """
        Loads a sqlite db file.

        Args:
            file:

        Returns:

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
        return board_position.BoardPosition(column, row)

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
            if pos.is_on_board():
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
        pos = pygame.mouse.get_pos()
        clicked_container = self.window.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self:
            return pos
        else:
            return None
