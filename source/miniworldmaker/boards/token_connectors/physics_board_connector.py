import miniworldmaker.tokens.sensors.token_pixelboardsensor as pixelboardsensor
import miniworldmaker.tokens.costumes.token_physics_costume_manager as physicsboardcostumemanager
import miniworldmaker.tokens.positions.token_physics_position_manager as physicspositionmanager
import miniworldmaker.boards.token_connectors.pixel_board_connector as pixelboard_connector
from miniworldmaker.board_positions import board_position
from miniworldmaker.tokens.physics import token_physics
import sys


class PhysicsBoardConnector(pixelboard_connector.PixelBoardConnector):

    count_tokens = 0

    def __init__(self, board, token):
        super().__init__(board, token)

    def add_token_to_board(self, position: board_position.BoardPosition):
        super().add_token_to_board(position)
        self.board.register_all_physics_handlers(self.token)

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
        self.register_physics_handlers(token, method)
