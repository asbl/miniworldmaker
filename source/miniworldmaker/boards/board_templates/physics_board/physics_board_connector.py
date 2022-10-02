import miniworldmaker.positions.position as board_position
import miniworldmaker.boards.board_templates.pixel_board.pixel_board_connector as pixelboard_connector
import miniworldmaker.boards.board_templates.physics_board.token_physics as token_physics
import miniworldmaker.boards.board_templates.physics_board.token_physics_position_manager as physicspositionmanager
import miniworldmaker.boards.board_templates.pixel_board.token_pixelboardsensor as token_pixelboardsensor


class PhysicsBoardConnector(pixelboard_connector.PixelBoardConnector):
    count_tokens = 0

    def __init__(self, board, token):
        super().__init__(board, token)

    @staticmethod
    def get_position_manager_class():
        return physicspositionmanager.PhysicsBoardPositionManager

    @staticmethod
    def get_board_sensor_class():
        return token_pixelboardsensor.TokenPixelBoardSensor
    
    def add_token_to_board(self):
        # add token.physics attribute with physics properties to token
        self.token.physics = token_physics.TokenPhysics(self.token, self.token.board)
        if hasattr(self.token, "set_physics_default_values"):
            self.token.set_physics_default_values()
        super().add_token_to_board()
        self.board.register_all_physics_collision_managers_for_token(self.token)
        self.token.physics._start()
        self.board.physics_tokens.append(self.token)
        if hasattr(self.token, "on_begin_simulation"):
            self.token.on_begin_simulation()
