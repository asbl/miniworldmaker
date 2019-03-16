from miniworldmaker import *
from miniworldmaker.actors.actor import Actor
import pygame
from collections import defaultdict
from typing import Union


class TileBasedBoard(AbstractBoard):

    def __init__(self, columns=20, rows=16, tile_size=20, tile_margin=0):
        super().__init__(columns=columns, rows=rows)
        self._tile_size = tile_size
        self._tile_margin = tile_margin
        self.set_size(self.tile_size, columns, rows, tile_margin)
        self._dynamic_actors_dict = defaultdict(list)  # the dict is regularly updated
        self._dynamic_actors = []  # List with all dynamic actors
        self._static_actors_dict = defaultdict(list)

    def _update_actors_positions(self) -> None:
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_colliding_actors(self, actor: Actor) -> list:
        self._update_actors_positions()
        colliding_actors = self.get_actors_at_location(actor.rect)
        if actor in colliding_actors:
            colliding_actors.remove(actor)
        return colliding_actors

    def get_actors_at_location(self, value: Union[pygame.Rect, tuple]) -> list:
        self._dynamic_actors_dict.clear()
        self._update_actors_positions()
        if type(value) == tuple:
            x, y = value[0], value[1]
        else:
            x, y = self.pixel_to_grid_position(value.topleft)
        actors = []
        if self.is_in_grid(self.rect):
            if self._dynamic_actors_dict[x, y]:
                actors.extend(self._dynamic_actors_dict[(x, y)])
            if self._static_actors_dict[x, y]:
                actors.extend(self._static_actors_dict[(x, y)])
        return actors

    def remove_actor(self, actor: Actor) -> None:
        if actor in self._dynamic_actors:
            self._dynamic_actors.remove(actor)
        if actor in self._static_actors_dict[(actor.x, actor.y)]:
            self._static_actors_dict[(actor.x, actor.y)].remove(actor)
        super().remove_actor(actor)

    def remove_actors_from_cell(self, cell: tuple)->None:
        """
        Entfernt alle Actors aus einer Zelle
        Parameters
        ----------
        cell : Die Zelle aus der der Akteur entfernt werden soll.

        Returns
        -------

        """
        for actor in self._dynamic_actors_dict[cell[0], cell[1]]:
            self.remove_actor(actor)
        for actor in self._static_actors_dict[cell[0], cell[1]]:
            self.remove_actor(actor)

    def add_actor(self, actor: Actor, position: tuple = None) -> Actor:
        if actor.is_static:
            self._static_actors_dict[(position[0], position[1])].append(actor)
        else:
            self._dynamic_actors.append(actor)
        super().add_actor(actor, position)
        if actor.size == (0, 0):
            actor.size = (self.tile_size, self.tile_size)
        actor.image_action("scale_x", False)
        actor.image_action("scale_y", False)
        actor.image_action("upscale_x", True)
        actor.image_action("upscale_y", True)
        return actor

    def update_actor(self, actor: Actor, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_actors_dict[(actor.x(), actor.y())].append(actor)
            if actor in self._dynamic_actors_dict:
                self._dynamic_actors_dict.pop(actor)
        else:
            self._dynamic_actors.append(actor)

    def is_empty_cell(self, position: tuple) -> bool:
        """
        Checks if cell is empty
        :param position: the position of the cell
        :return: True if cell is empty
        """
        if not self.get_actors_at_location(position):
            return True
        else:
            return False

    @staticmethod
    def get_neighbour_cells(position: tuple) -> list:
        """
        Gets a list with all neighbour cells
        :param position: The position of the cell
        :return: the neighbour cells as list
        """
        cells = []
        y_pos = position[0]
        x_pos = position[1]
        cells.append([x_pos + 1, y_pos])
        cells.append([x_pos + 1, y_pos + 1])
        cells.append([x_pos, y_pos + 1])
        cells.append([x_pos - 1, y_pos + 1])
        cells.append([x_pos - 1, y_pos])
        cells.append([x_pos - 1, y_pos - 1])
        cells.append([x_pos, y_pos - 1])
        cells.append([x_pos + 1, y_pos - 1])
        return cells

    def is_in_grid(self, value: Union[tuple, pygame.Rect]) -> bool:
        if type(value) == tuple:
            value = self.tile_to_rect(value)
        x, y = self.pixel_to_grid_position(value.center)
        if x > self.columns - 1:
            return False
        elif y > self.rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def is_at_border(self, actor : Actor) -> str:
        if actor.x == self.columns - 1:
            return "right"
        elif actor.y == self.rows - 1:
            return "bottom"
        elif actor.x == 0:
            return "left"
        elif actor.y == 0:
            return "top"
        else:
            return None
