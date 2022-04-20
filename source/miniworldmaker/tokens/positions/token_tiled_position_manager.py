import math
from typing import Tuple, Union

import pygame

import miniworldmaker.board_positions.tile_elements as tile_elements
import miniworldmaker.tokens.positions.token_position_manager as token_position_manager


class TiledBoardPositionManager(token_position_manager.TokenPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        self._scaled_size = (1, 1)

    def get_rect(self):
        if self.token.costume:
            rect = self.token.costume.image.get_rect()
        else:
            rect = pygame.Rect(0, 0, self.token.size[0], self.token.size[1])
        if self.token.board.is_tile(self.token.position):
            rect.topleft = tile_elements.Tile.from_position(self.token.position).to_pixel()
        if self.token.board.is_corner(self.token.position):
            rect.center = tile_elements.Corner.from_position(self.token.position).to_pixel()
        if self.token.board.is_edge(self.token.position):
            rect.center = tile_elements.Edge.from_position(self.token.position).to_pixel()
        return rect

    @property
    def size(self):
        if self.token.board:
            return (
                self.token.board.tile_size * self._scaled_size[0],
                self.token.board.tile_size * self._scaled_size[1],
            )
        else:
            return 0

    @size.setter
    def size(self, value: Union[int, Tuple]):
        if type(value) == int or type(value) == float:  # convert int to tuple
            value = (value, value)
        self._scaled_size = value
        self.token.costume.reload_transformations_after("all")

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.position
        x = destination[0] - pos[0]
        y = destination[1] - pos[1]
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                self.token.direction = math.degrees(math.atan(m)) - 90
            else:
                # destination is right
                self.token.direction = math.degrees(math.atan(m)) + 90
            return self.token.direction
        else:
            m = 0
            if destination[1] > self.token.position[1]:
                self.token.direction = 180
                return self.token.direction
            else:
                self.token.direction = 0
                return self.token.direction
