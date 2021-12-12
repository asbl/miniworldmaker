from miniworldmaker.tokens.costumes import token_physics_costume_manager as physicsboardcostumemanager
from miniworldmaker.tokens.positions import token_physics_position_manager as physicspositionmanager
from miniworldmaker.boards.token_connectors import pixel_board_connector as pixelboard_connector
from miniworldmaker.board_positions import board_position
from miniworldmaker.tokens.physics import token_physics
import miniworldmaker

class PhysicsBoardConnector(pixelboard_connector.PixelBoardConnector):

    count_tokens = 0

    def __init__(self, board, token):
        super().__init__(board, token)

    def add_token_to_board(self, position: board_position.BoardPosition):
        # add token.physics attribute with physics properties to token
        self.token.physics = token_physics.TokenPhysics(self.token, miniworldmaker.App.board)
        if hasattr(self.token, "set_physics_default_values"):
            self.token.set_physics_default_values()
        super().add_token_to_board(position)
        self.board.register_all_physics_collision_handlers_for_token(self.token)
        self.token.physics.start()
        self.board.physics_tokens.append(self.token)
        if hasattr(self.token, "on_begin_simulation"):
            self.token.on_begin_simulation()
            
    def add_position_manager_to_token(self, token, position):
        token.position_manager = physicspositionmanager.PhysicsBoardPositionManager(
            token, position)
        token._managers.append(token.position_manager)

    def add_board_costume_manager_to_token(self, token, image):
        token.costume_manager = physicsboardcostumemanager.PhysicsBoardCostumeManager(token, image)
        token._managers.append(token.costume_manager)

    def register_token_method(self, token, method: callable):
        """
        Bind a touching method to pymunk engine, e.g.: 
        if method on_touching_token
        is registered, in pymunk are following handlers registered:
        handler for (self.__class__, Token.__class_)
        handler for (self.__class__, player.class.__class__)
        handler for (self.__class__, wall.class.__class__)
        (because Player and Wall are subclasses of Token)
        """
        super().register_token_method(token, method)
        # Register physic collision methods
    
