from miniworldmaker.tokens.sensors import token_tiledboardsensor as tiledboardsensor
from miniworldmaker.tokens.costumes import token_tiled_costume_manager as tiledboardcostumemanager
from miniworldmaker.tokens.positions import token_tiled_position_manager as tiledpositionmanager
from miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.board_positions import board_position


class TiledBoardConnector(token_connector.TokenConnector):

    def add_token_to_board(self, position: board_position.BoardPosition):
        super().add_token_to_board(position)
        self.token.costume_manager.set_size()

    def add_board_sensor_to_token(self, token):
        token.board_sensor = tiledboardsensor.TokenTiledBoardSensor(token, self.board)
        token._managers.append(token.board_sensor)

    def add_board_costume_manager_to_token(self, token, image):
        token.costume_manager = tiledboardcostumemanager.TiledBoardCostumeManager(token, image)
        token._managers.append(token.costume_manager)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = tiledpositionmanager.TiledBoardPositionManager(token, position)
        token._managers.append(token.position_manager)
