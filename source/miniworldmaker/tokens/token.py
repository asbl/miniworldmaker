import math
from logging import *
from typing import Union
import pygame
from tools import image_renderer
from boards import board_position
from tokens import costume


class Token(pygame.sprite.DirtySprite):

    token_count = 0
    log = getLogger("Token")
    lookup = True

    def __init__(self):
        super().__init__()
        # private
        self._size = (0, 0)  # Tuple with size
        self._position: board_position = None
        self._on_board = False
        self._is_at_border = False
        self._at_borders_list = False
        self._flip_x = False
        Token.token_count += 1
        # public
        self.token_id = Token.token_count + 1
        self.is_static = True
        self.direction = 0
        self.orientation = 0
        self.board = None
        # costume
        self.costume = costume.Costume(self)
        self._image = self.costume.image
        self.costumes = [self.costume]
        self.init = 1

    def __str__(self):
        if self.board:
            return "Klasse: {0}; ID: {1}, Position: {2}".format(self.class_name, self.token_id, self.rect)
        else:
            return "Klasse: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._image = self.costume.image
            return self.costume.image

    @property
    def rect(self):
        try:
            if type(self.position == board_position.BoardPosition):
                return self.position.to_rect(rect=self.image.get_rect())
            else:
                raise TypeError("Wrong type for board position")
        except AttributeError as e:
            if self.board is None:
                raise ("ERROR: The actor {0} is not attached to a Board\n"
                               "Maybe you forgot to add the actor with the board.add_actor function ".format(self))

    def add_image(self, path: str) -> int:
        return self.costume.add_image(path)

    def add_costume(self, path: str) -> int:
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        self.costumes.append(new_costume)
        return len(self.costumes) - 1

    def switch_costume(self):
        index = self.costumes.index(self.costume)
        if index < len(self.costumes) - 1:
            index += 1
        else:
            index = 0
        self.costume = self.costumes[index]
        return self.costume

    def _next_sprite(self):
        if self.costume.is_animated:
            if self.board.frame % self.costume.animation_speed == 0:
                self.costume.next_sprite()

    @property
    def direction(self) -> int:
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        direction = self._value_to_direction(value)
        self._direction = direction
        self.dirty = 1

    @property
    def size(self):
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.dirty = 1

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        if type(value) == tuple:
            value = board_position.BoardPosition(value[0], value[1])
        self._position = value
        self.dirty = 1

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    # Methoden
    def act(self):
        """
        Überschreibe diese Methode in deinen eigenen Actor-Klassen
        """
        pass

    def listen(self, key, data=None):
        """
        Diese Methode sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    @property
    def x(self):
        """
        Gibt die x-Koordinate des Akteuers zurück.

        :param x: Gibt die x-Koordinate des Akteurs zurück.
        """
        return self.position[0]

    @x.setter
    def x(self, x):
        """
        Setzt die x-Koordinate der Akteurs.
        :param x: Die x-Koordinate die gesetzt werden soll.
        """
        self.position = (x, self.position[1])

    @property
    def y(self):
        """
        Gibt die y-Koordinate des Akteuers zurück.

        :param y: Gibt die y-Koordinate des Akteurs zurück
        """
        return self.position[1]

    @y.setter
    def y(self, y):
        """
        Setzt die y-Koordinate der Akteurs.

        :param y: Die y-Koordinate die gesetzt werden soll.
        """
        self.position = (self.position[0], y)

    def setup(self):
        """
        Sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    def update(self):
        self._next_sprite()

    def _value_to_direction(self, value) -> int:
        if value == "right":
            value = 0
        if value == "left":
            value = 180
        if value == "up":
            value = 90
        if value == "down":
            value = 270
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
        value = value % 360
        return value

    def remove(self):
        """
        Removes this actor from board
        """
        if self.board:
            self.board.remove_from_board(self)
        self.kill()
        del (self)

    def is_colliding(self):
        return self.board.is_colliding(self)

    def get_colliding_tokens(self):
        return self.board.get_colliding_tokens(self)

    def is_colliding_with(self, class_name):
        colliding_tokens = self.board.get_colliding_tokens(self)
        from boards import board
        return board.Board.filter_actor_list(colliding_tokens, class_name)

    def is_at_border(self):
        return self.board.borders(self.rect)

    def is_on_the_board(self):
        return self.board.is_on_board(self.rect)

    def get_event(self, event, data):
        pass

    @classmethod
    def register_subclasses(base):
        d = {}
        for cls in base.__subclasses__():
            d[cls.__name__] = cls
        print(d)
        return d