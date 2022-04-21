from math import radians, degrees

import miniworldmaker.board_positions.board_position as board_position
import miniworldmaker.tokens.positions.token_pixel_position_manager as pixel_position_manager
from miniworldmaker.exceptions.miniworldmaker_exception import PhysicsSimulationTypeError


class PhysicsBoardPositionManager(pixel_position_manager.PixelBoardPositionManager):
    def __init__(self, token, position):
        super().__init__(token, position)
        if self.size:
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
        if hasattr(self.token,
                   "physics") and self.token.physics.has_physics and not self.token.physics._is_in_update_mode() and value != pos:
            self.token.physics.dirty = 0
            self.token.physics.reload()
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

    def move_to(self, position: "board_position.Position"):
        self.center = position
        if hasattr(self.token, "physics"):
            self.token.physics.reload()

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        if self.token.physics._body:
            pymunk_direction = self.get_pymunk_direction(value)
            self.token.physics._body.angle = pymunk_direction
            super().set_direction((value + 360) % 360)
        else:
            super().set_direction(value)

    def get_pymunk_direction_from_miniworldmaker(self):
        mwm_direction = self._direction
        return self.get_pymunk_direction(mwm_direction)

    def get_pymunk_direction(self, value):
        mwm_direction = (value + 360) % 360
        direction = radians(mwm_direction)
        return direction

    def set_mwm_direction_from_pymunk(self):
        pymunk_dir_in_degrees = degrees(self.token.physics._body.angle)
        mwm_direction = (pymunk_dir_in_degrees + 360) % 360
        super().set_direction(mwm_direction)

    def impulse(self, direction:float, power:int):
        self.token.physics.impulse_in_direction(direction, power)

    def force(self, direction:float, power:int):
        self.token.physics.force_in_direction(direction, power)

    def set_simulation(self, simulation_type: str):
        if simulation_type in ["simulated", "manual", "static", None]:
            self.token.physics.simulation = simulation_type
            self.token.physics.reload()
        else:
            raise PhysicsSimulationTypeError()

    def set_velocity_y(self, value):
        self.token.physics.velocity_y = value

    def set_velocity_x(self, value):
        self.token.physics.velocity_x = value

    def set_velocity(self, value):
        self.token.physics.velocity_x, self.token.physics.velocity_y = value[0], value[1]

    def self_remove(self):
        self.token.physics._remove_from_space()
