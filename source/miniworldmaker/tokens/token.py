import math
from logging import *
from typing import Union
from miniworldmaker.tools.image_renderer import ImageRenderer
import pygame


class Token(pygame.sprite.DirtySprite):

    token_count = 0
    log = getLogger("Token")
    lookup = True

    def __init__(self):
        super().__init__()
        # private
        self._renderer = ImageRenderer()
        self._image = self._renderer.get_image()
        self._size = (0, 0)  # Tuple with size
        self._position = (0, 0)  # set by gamegrid.add_actor
        self._is_in_grid = False
        self._is_at_border = False
        self._is_touching_borders = False
        self._is_colliding = False
        self._colliding_tokens = []
        self._flip_x = False
        Token.token_count += 1
        # public
        self.token_id = Token.token_count + 1
        self.animation_speed = 60
        self.is_static = True
        self.is_animated = False
        self.direction = 0
        self.orientation = 0
        self.board = None
        self.init = 1

    def __str__(self):
        if self.board:
            return "Klasse: {0}; ID: {1}, Position: {2}".format(self.class_name, self.token_id, self.rect)
        else:
            return "Klasse: {0}; ID: {1}".format(self.class_name, self.token_id)

    def image_action(self, attribute: str, value: bool):
        self._renderer.image_actions[attribute] = value

    def set_upscale(self):
        self._renderer.image_actions["scale_x"] = False
        self._renderer.image_actions["scale_y"] = False
        self._renderer.image_actions["upscale"] = True

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._renderer.direction = self.direction
            self._renderer.size = self.size
            self._renderer.orientation = self.orientation
            self._renderer.flipped = self._flip_x
            self._image = self._renderer.get_image()
            return self._image

    @property
    def rect(self):
        try:
            return self.board.rect_to_position(self.position, self.image.get_rect())
        except AttributeError as e:
            if self.board is None:
                self.log.error("ERROR: The actor {0} is not attached to a Board\n"
                               "Maybe you forgot to add the actor with the board.add_actor function ".format(self))
            raise

    def add_image(self, path: str) -> pygame.Surface:
        return self._renderer.add_image(path)

    def clear(self):
        self._renderer = ImageRenderer()

    def _next_sprite(self):
        if self.board.frame % self.animation_speed == 0:
            self._renderer.next_sprite()

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
        self.changed()

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
        self.changed()

    def animate(self):
        """
        Startet eine Animation.
        """
        if not self.is_animated:
            self.is_animated = True

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, value: tuple):
        self._position = value
        self.changed()

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    # Methoden
    def act(self):
        """
        Überschreibe diese Methode in deinen eigenen Actor-Klassen
        """
        pass

    def stop(self):
        """
        Stopt die Animation eines Akteurs.
        """
        self.is_animated = False

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

    def changed(self):
        self.dirty = 1
        self._update_status()

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

    def _update_status(self):
        try:
            in_grid = self.on_the_board()
            if in_grid != self._is_in_grid:
                self._is_in_grid = in_grid
                self.board.get_event("in_grid", self)
            at_border = self.is_at_border()
            if at_border != self._is_at_border:
                self._is_at_border = at_border
                self.board.get_event("at_border", self)
            colliding = self.is_colliding()
            if colliding != self._is_colliding:
                new_colliding_tokens = self.get_colliding_tokens()
                self._is_colliding = colliding
                for col_partner in new_colliding_tokens:
                    if col_partner not in self._colliding_tokens:
                        col_partner._colliding_tokens.append(self)
                        self.get_event("collision", (self, col_partner))
                        self.board.get_event("collision", (self, col_partner))
        except AttributeError:
            pass

    def is_colliding(self):
        return self.board.is_colliding(self)

    def get_colliding_tokens(self):
        return self.board.get_colliding_tokens(self)

    def is_colliding_with(self, class_name):
        colliding_tokens = self.board.get_colliding_tokens(self)
        return Board.filter_actor_list(colliding_tokens, class_name)

    def is_at_border(self):
        return self.board.borders(self.rect)

    def on_the_board(self):
        return self.board.on_board(self.rect)

    def get_event(self, event, data):
        pass

    @classmethod
    def register_subclasses(base):
        d = {}
        for cls in base.__subclasses__():
            d[cls.__name__] = cls
        print(d)
        return d
