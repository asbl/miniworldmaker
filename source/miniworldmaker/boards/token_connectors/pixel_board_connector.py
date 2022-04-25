from miniworldmaker.tokens.sensors import token_pixelboardsensor as pixelboardsensor
from miniworldmaker.tokens.positions import token_pixel_position_manager as pixelpositionmanager
from miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.board_positions import board_position


class PixelBoardConnector(token_connector.TokenConnector):

    def __init__(self, board, token):
        super().__init__(board, token)
        self.board_sensor = pixelboardsensor.TokenPixelBoardSensor(token, board)

    def get_position_manager_class(self):
        return pixelpositionmanager.PixelBoardPositionManager

    def add_token_to_board(self, position: "board_position.Position"):
        super().add_token_to_board(position)


