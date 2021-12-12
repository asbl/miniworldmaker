from miniworldmaker.tokens.sensors import token_pixelboardsensor as pixelboardsensor
from miniworldmaker.tokens.costumes import token_pixel_costume_manager as pixelboardcostumemanager
from miniworldmaker.tokens.positions import token_pixel_position_manager as pixelpositionmanager
from  miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.board_positions import board_position


class PixelBoardConnector(token_connector.TokenConnector):

    def add_token_to_board(self, position: board_position.BoardPosition):
        super().add_token_to_board(position)

    def add_board_sensor_to_token(self, token):
        token.board_sensor = pixelboardsensor.TokenPixelBoardSensor(token, self.board)
        token._managers.append(token.board_sensor)

    def add_board_costume_manager_to_token(self, token, image):
        token.costume_manager = pixelboardcostumemanager.PixelBoardCostumeManager(token, image)
        token._managers.append(token.costume_manager)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = pixelpositionmanager.PixelBoardPositionManager(token, position)
        token._managers.append(token.position_manager)
