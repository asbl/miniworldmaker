from math import radians, degrees
from miniworldmaker.tokens.positions import token_pixel_position_manager as pixel_position_manager
from miniworldmaker.board_positions import board_position
from miniworldmaker.exceptions.miniworldmaker_exception import PhysicsSimulationTypeError


class PhysicsBoardPositionManager(pixel_position_manager.PixelBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        if not self.size:
            self.size = (40, 40)
        self.token.register(self.impulse)
        self.token.register(self.force)
        self.token.register(self.set_simulation)
        self.token.register(self.set_velocity_x)
        self.token.register(self.set_velocity_y)
        self.token.register(self.set_velocity)

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
            return self._direction

    def set_direction(self, value):
        if self.token.physics._body:
            pymunk_direction = self.get_pymunk_direction(value)
            self.token.physics._body.angle = pymunk_direction 
            super().set_direction((value + 360 ) % 360)
        else:
            super().set_direction(value)

    def get_pymunk_direction_from_miniworldmaker(self):
        mwm_direction = self._direction
        return self.get_pymunk_direction(mwm_direction)

    def get_pymunk_direction(self, value):
        mwm_direction  = (value + 360) % 360 
        direction = radians(mwm_direction)  
        return direction

    def set_mwm_direction_from_pymunk(self):
        pymunk_dir_in_degrees = degrees(self.token.physics._body.angle)
        mwm_direction = (pymunk_dir_in_degrees + 360  ) % 360  
        super().set_direction(mwm_direction)

    def impulse(self, direction=float, power=int):
        self.token.physics.impulse_in_direction(180 + direction, power)

    def force(self, direction=float, power=int):
        self.token.physics.force_in_direction(180 + direction, power)

    def set_simulation(self, simulation_type: str):
        if simulation_type in ["simulated", "manual", "static", None]:
            self.token.physics.simulation = simulation_type
        else:
            raise PhysicsSimulationTypeError()

    def set_velocity_y(self, value):
        self.token.physics.velocity_y = value

    def set_velocity_x(self, value):
        self.token.physics.velocity_x = value

    def set_velocity(self, value):
        self.token.physics.velocity_x, self.token.physics.velocity_y  = value[0], value[1]