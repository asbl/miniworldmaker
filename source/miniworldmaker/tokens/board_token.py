import math
from logging import *
from typing import Union
import pygame
from miniworldmaker.boards import board_position
from miniworldmaker.tokens import costume
from miniworldmaker.windows import miniworldwindow


class Token(pygame.sprite.DirtySprite):

    token_count = 0
    log = getLogger("Token")
    lookup = True

    def __init__(self, position = None):
        self.board = None
        super().__init__()
        self.costume = None

        # private
        self._size = (0, 0)  # Tuple with size
        self._position: board_position = position
        self._on_board = False
        self._is_at_border = False
        self._at_borders_list = False
        self._is_flipped = False
        Token.token_count += 1
        self._direction = 0
        # public

        self.last_position = (0,0)
        self.last_direction = 90
        self.token_id = Token.token_count + 1
        self.is_static = True
        # costume
        self.costume = costume.Costume(self)
        self._image = pygame.Surface((1, 1))
        self.costumes = [self.costume]
        self.costume.is_upscaled = True
        self.costume.orientation = 0
        self.init = 1
        self.speed = 0
        self.registered_events = ["mouse_left", "mouse_right"]
        if position is not None:
            self.board = miniworldwindow.MiniWorldWindow.board
            self.board.add_to_board(self, position)
        else:
            board = None
        self._dirty = 1


    @property
    def is_flipped(self):
        return self.costume.is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self.costume._is_flipped = value
        if self.is_flipped is True:
            self.costume.enabled_image_actions["flip"] = True
            self.costume.call_action("flip")
        else:
            self.costume.enabled_image_actions["flip"] = False
            self.costume.call_action("flip")

    def __str__(self):
        if self.board:
            return "{0}-Object, ID: {1} at pos {2}".format(self.class_name, self.token_id, self.position)
        else:
            return "**: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._image = self.costume.image
            return self.costume.image
    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.board:
            self.board.dirty = 1

    @property
    def rect(self):
        self._rect = self.position.to_rect(rect=self.image.get_rect())
        if self.dirty == 1:
            return self._rect
        else:
            return self._rect

    def add_image(self, path: str) -> int:
        return self.costume.add_image(path)

    def add_costume(self, path: str) -> costume.Costume:
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        new_costume.orientation = self.costume.orientation
        self.costumes.append(new_costume)
        return new_costume

    def switch_costume(self, index=-1) -> costume.Costume:
        """Switches costume

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: The new costume

        """
        if index == -1:
            index = self.costumes.index(self.costume)
            if index < len(self.costumes) - 1:
                index += 1
            else:
                index = 0
        else:
            index = index
        self.costume = self.costumes[index]
        self.costume.dirty = 1
        self.costume.changed_all()
        self.dirty = 1
        return self.costume

    def add_to_board(self, board, position: board_position.BoardPosition):
        try:
            self.board = board
            self.position = position
            self.costume.changed_all()
            self.dirty = 1
            if self.init != 1:
                raise UnboundLocalError("Init was not called")
        except UnboundLocalError:
            raise

    @property
    def direction(self) -> int:
        """ Sets direction the token is oriented

            0°:  East, x degrees clock-wise otherwise
            You can also set the direction by String ("forward", "up", "down", ...
        """
        return (self._direction + 180) % 360 - 180

    @direction.setter
    def direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        self.dirty = 1
        if self.costume:
            self.costume.call_action("rotate")
        if self.board:
            self.board.window.send_event_to_containers("actor_changed_direction", self)

    @property
    def size(self) -> tuple:
        """Size of the token

        """
        return self._size

    @size.setter
    def size(self, value :tuple):
        self._size = value
        self.dirty = 1
        self.costume.call_action("scale")

    @property
    def position(self) -> board_position.BoardPosition:
        """
        The position of the token is tuple (x, y)
        """
        return self._position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        self.last_position = self.position
        if type(value) == tuple:
            value = board_position.BoardPosition(value)
        self._position = value
        self.dirty = 1
        if self.board:
            self.board.window.send_event_to_containers("actor_moved", self)

    @property
    def x(self):
        """int: The x-value of an token
        """
        return self._position[0]

    @x.setter
    def x(self, value):
        self.position = (value, self.y)

    @property
    def y(self):
        """int: The x-value of an token
        """
        return self._position[1]

    @y.setter
    def y(self, value):
        self.position = (self.x, value)

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    # Methoden
    def act(self):
        """Custom acting

        This method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def update(self):
        if self.costume.is_animated:
            self.costume.update()

    def _value_to_direction(self, value) -> int:
        if value == "top" or value == "up":
            value = 0
        if value == "left":
            value = 270
        if value == "right":
            value = 90
        if value == "down":
            value = 180
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
        value = value % 360
        return value

    def remove(self):
        """Removes this actor from board
        """
        if self.board:
            self.board.remove_from_board(self)
        self.kill()
        del (self)

    def get_event(self, event, data):
        pass

    @classmethod
    def register_subclasses(base):
        d = {}
        for cls in base.__subclasses__():
            d[cls.__name__] = cls
        return d
