from math import radians
import miniworldmaker.tokens.positions.token_pixel_position_manager as pixel_position_manager
from miniworldmaker.board_positions import board_position


class PhysicsBoardPositionManager(pixel_position_manager.PixelBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        if not self.size:
            self.size = (40, 40)
        self.token.board.token_handler.register_token_method(self.token, self.impulse)

    def set_position(self, value):
        pos = super().set_position(value)
        if hasattr(self.token, "physics"):
            self.token.physics.dirty = 1
        return pos

    def set_center(self, value):
        pos = super().set_center(value)
        if hasattr(self.token, "physics"):
            self.token.physics.dirty = 1
        return pos

    def set_size(self, value):
        super().set_size(value)
        if hasattr(self.token, "physics"):
            self.token.physics.dirty = 1

    def move_to(self, position: board_position.BoardPosition):
        self.center = position
        if hasattr(self.token, "physics"):
            self.token.physics.reload()

    def set_direction(self, value):
        if self.token.physics._body:
            self.token.physics._body.angle = radians(value)
        else:
            super().set_direction(value)

    def set_direction_from_pymunk(self, value):
        super().set_direction(value)

    def impulse(self, direction=float, power=int):
        self.token.physics.impulse_in_direction(direction, power)
