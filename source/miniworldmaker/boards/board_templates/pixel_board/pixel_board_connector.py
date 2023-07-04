from miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.boards.board_templates.pixel_board import token_pixel_position_manager as pixelpositionmanager, \
    token_pixelboardsensor as pixelboardsensor


class PixelBoardConnector(token_connector.TokenConnector):

    def __init__(self, board, token):
        super().__init__(board, token)

    @staticmethod
    def get_position_manager_class():
        return pixelpositionmanager.PixelBoardPositionManager

    @staticmethod
    def get_board_sensor_class():
        return pixelboardsensor.TokenPixelBoardSensor
