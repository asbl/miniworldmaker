from math import radians, degrees
import miniworldmaker.tokens.positions.token_pixel_position_manager as pixel_position_manager
from miniworldmaker.board_positions import board_position
from miniworldmaker.exceptions.miniworldmaker_exception import PhysicsSimulationTypeError


class PhysicsBoardPositionManager(pixel_position_manager.PixelBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        if not self.size:
            self.size = (40, 40)
        self.token.board.token_handler.register_token_method(self.token, self.impulse)
        self.token.board.token_handler.register_token_method(self.token, self.set_simulation)

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

    def get_direction(self):
        if hasattr(self.token, "physics") and self.token.physics._body:
            return degrees(self.token.physics._body.angle) 
        else:
            return super().get_direction()

    def set_direction(self, value):
        if self.token.physics._body:
            self.token.physics._body.angle = radians(value)
        else:
            super().set_direction(value)

        
    def get_direction_from_miniworldmaker(self):
        return super().get_direction()

    def set_direction_from_pymunk(self, value):
        super().set_direction(value)

    def impulse(self, direction=float, power=int):
        self.token.physics.impulse_in_direction(direction, power)

    def set_simulation(self, simulation_type : str):
        if simulation_type in ["simulated", "manual", "static", None]:
            self.token.physics.simulation = simulation_type
        else:
            raise PhysicsSimulationTypeError()
