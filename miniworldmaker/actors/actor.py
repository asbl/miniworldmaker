# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""
from typing import Union
import math
import pygame
from miniworldmaker import *
from miniworldmaker.tools.image_renderer import ImageRenderer
from logging import *


class Actor(pygame.sprite.DirtySprite):

    actor_count = 0
    log = getLogger("Actor")

    def __init__(self):
        super().__init__()
        # private
        self._renderer = ImageRenderer()
        self._image = self._renderer.get_image()
        self._size = (0, 0)  # Tuple with size
        self._position = (0, 0) # set by gamegrid.add_actor
        self.actor_id = Actor.actor_count + 1
        # protected
        self.__flip_x = False
        self.__is_in_grid = False
        self.__is_at_border = False
        self.__is_touching_borders = False
        self.__is_colliding = False
        self.__colliding_actors = []
        Actor.actor_count += 1
        # public
        self.animation_speed = 60
        self.is_static = False
        self.is_animated = False
        self.direction = 0
        self.orientation = 0
        self.grid = None
        self.init = 1

    def __str__(self):
        if self.grid:
            return "Klasse: {0}; ID: {1}, Position: {2}".format(self.class_name, self.actor_id, self.rect)
        else:
            return "Klasse: {0}; ID: {1}".format(self.class_name, self.actor_id)

    def image_action(self, attribute : str, value : bool):
            self._renderer.image_actions[attribute] = value

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._renderer.direction = self.direction
            self._renderer.size = self.size
            self._renderer.orientation = self.orientation
            self._renderer.flipped = self.__flip_x
            self._image = self._renderer.get_image()
            return self._image

    @property
    def rect(self):
        try:
            return self.grid.rect_to_position(self.position, self.image.get_rect())
        except AttributeError as e:
            if self.grid is None:
                self.log.error("ERROR: The actor {0} is not in a grid\n"
                                "Maybe you forgot to add the actor with the grid.add_actor function ".format(self))
            raise

    def add_image(self, path: str) -> pygame.Surface:
        return self._renderer.add_image(path)

    def clear(self):
        self._renderer = ImageRenderer()

    def _next_sprite(self):
        if self.grid.frame % self.animation_speed == 0:
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

    def flip_x(self):
        """
        Spiegelt das Bild des Akteurs über die y-Achse.
        Der Akteur selbst wird dabei um 180° gedreht.
        """
        if not self.__flip_x:
            self.__flip_x = True
        else:
            self.__flip_x = False
        self.turn_left(180)

    def set_bounding_box_size(self, value):
        """
        Legt die Größe der umgebenen Bounding-Box fest.

        :param value: Eine Größe (width, height) als Tupel.
        """
        self.__bounding_box_size = value

    def listen(self, key, data = None):
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

    def turn_left(self, degrees: int = 90) -> int:
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        self.log.info("turn left {0} , {1}".format(self.direction, degrees))
        direction = self.direction + degrees
        self.direction = direction
        return self.direction

    def turn_right(self, degrees: int = 90):
        """
        Der Actor dreht sich um 90° nach rechts.

        :param degrees: Richtung in Grad.

        :return: Neue Richtung in Grad.
        """
        self.log.info("turn right {0} , {1}".format(self.direction, degrees))
        direction = self.direction - degrees
        self.direction = direction
        return self.direction

    def move(self, *, distance : int = 1, direction: Union[str, int] = "forward") -> tuple:
        self.direction = self._value_to_direction(direction)
        destination = self.look(distance = distance, direction = direction)
        self.position = self.grid.pixel_to_grid_position(destination.topleft)
        self.log.info("Move to position {0}; Direction {1}".format(self.position, self.direction))
        return self.position

    def look(self, *, distance: int = 1, direction: Union[str, int] = "here", ) -> pygame.Rect:
        if direction == "here":
            return self.rect
        else:
            direction = self._value_to_direction(direction)
            x = (self.position[0] + round(math.cos(math.radians(direction)) * distance))
            y = (self.position[1] - round(math.sin(math.radians(direction)) * distance))
            return self.grid.rect_to_position((x, y), self.rect)

    def look_forward(self, distance: int = 1) -> pygame.Rect:
        return self.look(direction="forward", distance = distance)

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
        Removes this actor from grid
        """
        if self.grid:
            self.grid.remove_actor(self)
        self.kill()
        del (self)

    def _update_status(self):
        try:
            in_grid = self.is_in_grid()
            if in_grid != self.__is_in_grid:
                self.__is_in_grid = in_grid
                self.grid.get_event("in_grid", self)
            at_border = self.is_at_border()
            if at_border != self.__is_at_border:
                self.__is_at_border = at_border
                self.grid.get_event("at_border", self)
            colliding = self.is_colliding()
            if colliding != self.__is_colliding:
                colliding_actors = self.get_colliding_actors()
                self.__is_colliding = colliding
                self.__collision_partners = None
                for col_partner in colliding_actors:
                    if col_partner not in self.__colliding_actors:
                        col_partner.__colliding_actors.append(self)
                        self.get_event("collision", (self, col_partner))
                        self.grid.get_event("collision", (self, col_partner))
        except AttributeError:
            pass

    def is_colliding(self):
        return self.grid.is_colliding(self)

    def get_colliding_actors(self):
        return self.grid.get_colliding_actors(self)

    def is_colliding_with(self, class_name):
        colliding_actors = self.grid.get_colliding_actors(self)
        return AbstractBoard.filter_actor_list(colliding_actors, class_name)

    def is_at_border(self):
        return self.grid.is_at_border(self.rect)

    def is_in_grid(self):
        return self.grid.is_in_grid(self.rect)

    def get_event(self, event, data):
        pass