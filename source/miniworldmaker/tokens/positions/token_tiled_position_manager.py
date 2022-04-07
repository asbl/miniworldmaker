from typing import Tuple, Union
import pygame
import math
from miniworldmaker.exceptions.miniworldmaker_exception import SizeOnTiledBoardError
import miniworldmaker.tokens.positions.token_position_manager as token_positionmanager


class TiledBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        self._scaled_size = (1, 1)

    def draw_position(self):
        x = self.token.x * self.token.board.tile_size + (self.token.board.tile_size - self.size[0]) / 2
        y = self.token.y * self.token.board.tile_size + (self.token.board.tile_size - self.size[1]) / 2
        return (x, y)

    @property
    def rect(self):
        pos = self.draw_position()
        return pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])

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
