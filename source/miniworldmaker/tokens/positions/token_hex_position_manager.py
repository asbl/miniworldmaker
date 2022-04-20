import pygame

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.board_positions.hex_elements as hex_elements
import miniworldmaker.tokens.positions.token_tiled_position_manager as tiled_positionmanager


class HexBoardPositionManager(tiled_positionmanager.TiledBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)

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

    def get_position(self) -> "board_position.Position":
        return self._position

    def set_direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.token.costume.reload_transformations_after("all")
