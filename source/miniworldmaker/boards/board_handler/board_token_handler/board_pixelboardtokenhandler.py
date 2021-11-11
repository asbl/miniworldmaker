import miniworldmaker.tokens.sensors.token_pixelboardsensor as pixelboardsensor
import miniworldmaker.tokens.costumes.token_pixel_costume_manager as pixelboardcostumemanager
import miniworldmaker.tokens.positions.token_pixel_position_manager as pixelpositionmanager
import miniworldmaker.boards.board_handler.board_token_handler.board_token_handler as board_tokenhandler
from miniworldmaker.board_positions import board_position


class PixelBoardTokenHandler(board_tokenhandler.BoardTokenHandler):

    def add_token_to_board(self, token, position: board_position.BoardPosition):
        super().add_token_to_board(token, position)

    def add_board_sensor_to_token(self, token):
        token.board_sensor = pixelboardsensor.TokenPixelBoardSensor(token, self.board)
        token._managers.append(token.board_sensor)

    def add_board_costume_manager_to_token(self, token, image):
        token.costume_manager = pixelboardcostumemanager.PixelBoardCostumeManager(token, image)
        token._managers.append(token.costume_manager)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = pixelpositionmanager.PixelBoardPositionManager(token, position)
        token._managers.append(token.position_manager)
