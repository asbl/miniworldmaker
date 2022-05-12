import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.hex_elements as hex_elements
import miniworldmaker.tokens.positions.token_tiled_position_manager as tiled_positionmanager
import miniworldmaker.board_positions.board_direction as board_direction
from miniworldmaker.exceptions.miniworldmaker_exception import MoveInDirectionTypeError
from typing import Union


class HexBoardPositionManager(tiled_positionmanager.TiledBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        if position is not None:
            self._position = hex_elements.CubeCoord.create(position)
        else:
            self._position = hex_elements.CubeCoord.create((0, 0))

    def get_rect(self):
        if self.token.costume:
            rect = self.token.costume.image.get_rect()
        else:
            rect = pygame.Rect(0, 0, self.token.size[0], self.token.size[1])
        if self.token.board.is_tile(self.token.position):
            topleft = hex_elements.HexTile.from_position(self.token.position).to_pixel()
            if self._scaled_size != (1, 1):
                shift_x = (self.size[0] - self.token.board.get_tile_width()) / 2
                shift_y = (self.size[1] - self.token.board.get_tile_height()) / 2
                pos = board_position.Position(shift_x, shift_y)
                topleft = topleft - pos
            rect.topleft = topleft

        if self.token.board.is_corner(self.token.position):
            rect.center = hex_elements.HexCorner.from_position(self.token.position).to_pixel()
        if self.token.board.is_edge(self.token.position):
            rect.center = hex_elements.HexEdge.from_position(self.token.position).to_pixel()
        return rect

    @property
    def size(self):
        if self.token.board:
            return (
                self.token.board.get_tile_width() * self._scaled_size[0] + self.token.board.get_tile_width() // 10,
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

    def get_position(self) -> "hex_elements.CubeCoord":
        """Position is stores as CubeCoord on HexBoard
        """
        return self._position
    

    def set_position(self, value : Union[tuple, "board_position.BoardPosition"]) -> "hex_elements.CubeCoord":
        self.last_position = self.position
        self.last_direction = self.direction
        self._position = hex_elements.CubeCoord.create(value)
        if self.last_position != self._position:
            self.token.dirty = 1
            if self.token.board:
                self.token.board.app.event_manager.send_event_to_containers("token_moved", self.token)
        return self.position

    def set_direction(self, value):
        self.last_direction = self.direction
        direction = board_direction.Direction.create(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.token.costume.reload_transformations_after("all")

    def move_in_direction(self, direction: Union[int, str, "board_position.Position", tuple], distance=1):
        old_direction = self.token.direction
        direction = board_direction.Direction.create_from_token(self.token, direction).value
        self.set_direction(direction)
        self.move(distance)
        self.direction = old_direction
        return self
