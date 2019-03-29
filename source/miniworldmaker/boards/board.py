import logging
from typing import Union
import os
import pygame
from containers import container
from windows import miniworldwindow as window
from tools import image_renderer
from tools import db_manager
from tokens import board_token


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
        """
        initializes a new GameGrid
        Args:
            columns: The number of columns
            rows: The number of rows
        """
        super().__init__(self)
        pygame.init()
        # public
        self.active_token = None
        self.is_running = True
        # private
        self._speed = 60
        self._renderer = image_renderer.ImageRenderer()
        self.set_image_action("info_overlay", False)
        self.set_image_action("scale_x", True)
        self.set_image_action("scale_y", True)
        self.set_image_action("upscale", False)
        self._tokens = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._key = 0
        self._animated = False
        self._grid = []
        self._tile_size = 1
        self._tile_margin = 0
        self._columns, self._rows = columns, rows
        self.set_size(self.tile_size, columns, rows, self.tile_margin)
        # protected
        self.dirty = 1
        self.__frame = 0
        self.__tick = 0
        self.__clock = pygame.time.Clock()
        self.__last_update = pygame.time.get_ticks()
        # Init graphics
        self._image = pygame.Surface((0, 0))
        self.dirty = 1
        self._window = window.MiniWorldWindow("MiniWorldMaker")
        self._window.add_container(self, "main")

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
                 margin: int = 0):
        """
        Sets size of a gamegrid
        :param tile_size: The tile_size in pixels
        :param columns: The number of columns
        :param rows: The number of rows
        :param margin: the margin between tiles
        """
        self._tile_size = tile_size
        self._columns = columns
        self._rows = rows
        self._tile_margin = margin
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
        """
        Returns events triggered by events.
        :param event: The event
        :param data: The data of the event
        """
        pass

    def is_colliding(self, actor) -> bool:
        colliding_tokens = self.get_colliding_tokens(actor)
        if colliding_tokens:
            return True
        else:
            return False

    @property
    def width(self) -> int:
        """
        :return: Returns the width of the grid
        """
        if self.dirty == 0:
            return self._container_width
        else:
            self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
            return self._container_width

    @property
    def height(self) -> int:
        """
        :return: Returns the height of the grid
        """
        if self.dirty == 0:
            return self._container_height
        else:
            self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
            return self._container_height

    @property
    def window(self) -> window.MiniWorldWindow:
        """
        :return: returns the parent windows
        """
        return self._window

    @property
    def tile_size(self):
        """
        :return: The Tile size in pixels
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value: int):
        """ Sets the tile-size"""
        self._tile_size = value

    @property
    def tile_margin(self) -> int:
        """
        :return: The margin between tiles
        """
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
        """
        :return: number of columns of the grid
        """
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.dirty = 1

    @property
    def tokens(self):
        """
        :return: A list of all actors
        """
        return self._tokens

    @property
    def frame(self) -> int:
        """
        Returns the actual frame
        :return: the value of actual frame
        """
        return self.__frame

    @property
    def class_name(self) -> str:
        """
        :return: The Class Name of Actor
        """
        return self.__class__.__name__

    def set_image_action(self, attribute: str, value: bool):
        self._renderer.image_actions[attribute] = value

    def add_image(self, path: str) -> pygame.Surface:
        """
        :param img_path: The path to the image
        :return: The image
        """
        return self._renderer.add_image(path)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._renderer.size = (self._container_width, self._container_height)
            self._renderer.tile_size = self.tile_size
            self._renderer.margin = self.tile_margin
            _image = self._renderer.get_image()
            self._image = _image
            return _image

    def add_to_board(self, token: board_token.Token, board_position: tuple) -> board_token.Token:
        """
        adds actor to grid
        :param token: the actor as subclass of Actor
        :param board_position: the position in the grid
        :return: The Actor
        """
        self.tokens.add(token)
        if type(board_position) == tuple:
            token.position = board_position
        else:
            raise AttributeError("Position has wrong type" + str(type(board_position)))
        token.board = self
        token.dirty = 1
        if token.init != 1:
            raise UnboundLocalError("Init was not called")
        self.window.send_event_to_containers("Added token", token)
        return token

    def get_token_by_pixel(self, pixel: tuple) -> list:
        """
        Returns all players who have a certain pixel in common
        :param pixel: The pixel-coordinates
        :return: All actors as list
        """
        actors = []
        for actor in self.tokens:
            if actor.rect.collidepoint(pixel):
                actors.append(actor)
        return actors

    def get_tokens_in_area(self, value: Union[pygame.Rect, tuple], actor_type=None) -> list:
        """
        Gets all actors at location
        :param value: Either a tuple with cordinates in the grid or a Rect
        :param actor_type: Filters actor by type (e.g. all <Player>-Objects at position)
        :return:
        """
        actors = []
        if type(value) == tuple:
            value = pygame.Rect(value[0], value[1], 1, 1)
        for actor in actors:
            if actor.rect.colliderect(value):
                actors.append(actor)
        if actor_type is not None:
            actors = self.filter_actor_list(actors, actor_type)
        return actors

    def remove_actors_from_location(self, location: Union[tuple, pygame.Rect], actor_type=None):
        """
        Removes actor from an area or position
        :param location: The location can be either a Rect or a tuple with grid coordinates
        :param actor_type: Filters actor by type (e.g. all <Player>-Objects at position)
        """
        actors = []
        if type(location) == tuple:
            location = pygame.Rect(location[0], location[1], 1, 1)
        actors = self.get_tokens_in_area(location)
        if actor_type is not None:
            actors = self.filter_actor_list(actors, actor_type)
        for actor in actors:
            self.remove_from_board(actor)

    def remove_from_board(self, actor: board_token.Token):
        if actor:
            self.tokens.remove(actor)
            actor.board = None

    def remove_all_actors(self):
        """
        Entfernt alle Akteure aus dem Grid.
        """
        for actor in self.tokens:
            self.remove_from_board(actor)

    def reset(self):
        self.dirty = 1

    def on_board(self, value: Union[tuple, pygame.Rect]) -> bool:
        if type(value) == tuple:
            value = self.get_rect_from_board_position(value)
        top_left_x, top_left_y, right, top = value.topleft[0], \
                                             value.topleft[1], \
                                             value.right, \
                                             value.top
        if top_left_x < 0 or top_left_y < 0 or right > self.width or top > self.height:
            return False
        else:
            return True

    def borders(self, actor):
        pass

    def get_colliding_tokens(self, actor) -> list:
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
        self.window.show()

    def update(self):
        if self.is_running:
            self._act_all()
        self.__frame = self.__frame + 1
        for actor in self.tokens:
            actor.update()
        self._call_collision_events()
        if self.__frame == 100:
            self.__frame = 0
        self.__clock.tick(60)

    def _call_collision_events(self):
        pass

    def _act_all(self):
        self.__tick = self.__tick + 1
        if self.__tick > 60 - self.speed:
            for actor in self.tokens:
                actor.act()
            self.act()
            self.__tick = 0

    def pass_event(self, event, data=None):
        if event != "collision":
            for actor in self.tokens:
                actor.get_event(event, data)
        if event == "collision":
            for actor in self.tokens:
                if data[0] == actor:
                    actor.get_event("collision", data[1])
                elif data[1] == actor:
                    actor.get_event("collision", data[0])
        if event == "mouse_left":
            if self.get_token_by_pixel(data):
                self.set_active_token(self.get_token_by_pixel(data)[0])

    def set_active_token(self, token: board_token.Token):
        self.active_token = token
        token.changed()
        self.window.send_event_to_containers("active_token", token)
        return token

    def act(self):
        """
        Überschreibe diese Methode in deinen Kind-Klassen
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
                    board.add_to_board(token=token_instance, board_position=(tokens[1], tokens[2]))
        print(board)
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

    def get_rect_from_board_position(self, board_position: tuple, rect: pygame.Rect = None) -> pygame.Rect:
        if rect is None:
            new_rect = pygame.Rect(0, 0, self.tile_size, self.tile_size)
        else:
            new_rect = pygame.Rect(0, 0, rect.width, rect.height)
        # board position to pixel
        pixel_x = board_position[0] * self.tile_size + board_position[0] * self.tile_margin + self.tile_margin
        pixel_y = board_position[1] * self.tile_size + board_position[1] * self.tile_margin + self.tile_margin
        new_rect.topleft = (pixel_x, pixel_y)
        return new_rect

    def get_board_position_from_pixel(self, position: tuple) -> tuple:
        column = (position[0] - self.tile_margin) // (self.tile_size + self.tile_margin)
        row = (position[1] - self.tile_margin) // (self.tile_size + self.tile_margin)
        return column, row

    def get_board_position_from_rect(self, position: pygame.Rect) -> tuple:
        position = position.topleft
        return self.get_board_position_from_pixel(position)

    def get_color(self, board_position):
        return image_renderer.color_at(board_position)
