import math
from typing import Tuple, Union

import miniworldmaker.boards.board_templates.tiled_board.tile_elements as tile_elements
import miniworldmaker.tokens.managers.token_position_manager as token_position_manager
import miniworldmaker.positions.position as board_position
import miniworldmaker.positions.direction as board_direction
import miniworldmaker.appearances.costume as costume
import miniworldmaker.boards.board_templates.tiled_board.tile as tile_mod
import miniworldmaker.boards.board_templates.tiled_board.corner as corner_mod
import miniworldmaker.boards.board_templates.tiled_board.edge as edge_mod


class TiledBoardPositionManager(token_position_manager.TokenPositionManager):
    def __init__(self, token, board):
        super().__init__(token, board)
        self._scaled_size = (1, 1)

    def get_global_rect(self):
        rect = super().get_global_rect()
        if self.token.board.is_tile(self.token.position):
            rect.topleft = tile_mod.Tile.from_position(self.token.position, self.token.board).to_pixel()
            return rect
        elif self.token.board.is_corner(self.token.position):
            rect.center = corner_mod.Corner.from_position(self.token.position, self.token.board).to_pixel()
            return rect
        elif self.token.board.is_edge(self.token.position):
            rect.center = edge_mod.Edge.from_position(self.token.position, self.token.board).to_pixel()
            return rect
        else:
            rect.topleft = (-self.size[0], -self.size[1])
        return rect

    def get_local_rect(self):
        rect = self.get_global_rect()
        return rect

    def get_size(self):
        if self.token.board:
            return (
                self.token.board.tile_size * self._scaled_size[0],
                self.token.board.tile_size * self._scaled_size[1],
            )
        else:
            return 0

    def set_size(self, value: Union[int, Tuple], scale=True):
        if type(value) == int or type(value) == float:  # convert int to tuple
            value = (value, value)
        if scale and value != self._scaled_size and self.token.costume:
            self._scaled_size = value
            self.token.costume.set_dirty("scale", costume.Costume.RELOAD_ACTUAL_IMAGE)

    def set_center(self, value):
        self.position = value


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

    def move_towards_position(self, position, distance=1):
        tkn_center = board_position.Position.create(self.token.position)
        if tkn_center.is_close(position):
            return self
        else:
            direction = board_direction.Direction.from_two_points(self.token.position, position).value
            self.set_direction(direction)
            self.move(distance)
            return self
