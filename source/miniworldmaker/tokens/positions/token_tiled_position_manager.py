import pygame
import math
from miniworldmaker.exceptions.miniworldmaker_exception import SizeOnTiledBoardError
import miniworldmaker.tokens.positions.token_position_manager as token_positionmanager

class TiledBoardPositionManager(token_positionmanager.TokenPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        
        
    def draw_position(self):
        return (self.token.x * self.token.board.tile_size, self.token.y * self.token.board.tile_size)

    @property
    def rect(self):
        return pygame.Rect(self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1])

    @property
    def size(self):
        if self.token.board:
            return (self.token.board.tile_size, self.token.board.tile_size)
        else:
            return 0

    @size.setter
    def size(self, value):
        raise SizeOnTiledBoardError()

    def point_towards_position(self, destination) -> float:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        """
        pos = self.token.position
        x = (destination[0] - pos[0])
        y = (destination[1] - pos[1])
        if x != 0:
            m = y / x
            if x < 0:
                # destination is left
                self.token.direction = (math.degrees(math.atan(m)) - 90)
            else:
                # destination is right
                self.token.direction = (math.degrees(math.atan(m)) + 90)
            return self.token.direction
        else:
            m = 0
            if destination[1] > self.token.position[1]:
                self.token.direction = 180
                return self.token.direction
            else:
                self.token.direction = 0
                return self.token.direction