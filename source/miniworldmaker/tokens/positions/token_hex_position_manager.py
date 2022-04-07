import pygame
import math
from miniworldmaker.exceptions.miniworldmaker_exception import SizeOnTiledBoardError
from miniworldmaker.tokens.positions import token_tiled_position_manager as tiled_positionmanager
from miniworldmaker.board_positions import board_position


class HexBoardPositionManager(tiled_positionmanager.TiledBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)

    def draw_position(self):
        coord = self.token.board.to_pixel(self.position)
        if hasattr(self.token, "inner") and self.token.inner:
            x,y = self.token.board.get_tile(self.token.position).to_pixel()
            #x = coord[0] + (self.token.board.get_tile_width() - self.size[0]) / 2
            #y = coord[1] + (self.token.board.get_tile_height() - self.size[1]) / 2
        else:
            x, y = coord[0], coord[1]
        if hasattr(self.token, "corner"):
            x, y = self.token.board.get_corner_from_tile(self.position, self.token.corner).get_position()
            # move to center
            x -= self.token.size[0] / 2
            y -= self.token.size[1] / 2
        if hasattr(self.token, "edge") and self.token.edge in range(6):
            x, y = self.token.board.to_edge(self.position, self.token.edge)
        return board_position.Position(x, y)

    @property
    def rect(self):
        pos_x, pos_y = self.draw_position()
        # if hasattr(self.token, "inner") and self.token.inner:
        #    pos_x = pos_x + offset
        #    pos_y = pos_y + offset
        return pygame.Rect(pos_x, pos_y, self.size[0], self.size[1])

    @property
    def size(self):
        if self.token.board:
            return (
                self.token.board.get_tile_width() * self._scaled_size[0],
                self.token.board.get_tile_height() * self._scaled_size[1],
            )
        else:
            return 0

    @size.setter
    def size(self, value):
        if type(value) == int or type(value) == float:  # convert int to tuple
            value = (value, value)
        self._scaled_size = value
        self.token.costume.reload_transformations_after("all")