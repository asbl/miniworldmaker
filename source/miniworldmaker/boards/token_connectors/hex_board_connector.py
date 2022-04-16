from appearances import hex_costume
from appearances import costumes_manager
from tokens.sensors import token_tiledboardsensor as tiledboardsensor
from tokens.positions import token_hex_position_manager as hexpositionmanager
from boards.token_connectors import tiled_board_connector


class HexBoardConnector(tiled_board_connector.TiledBoardConnector):
    def add_board_sensor_to_token(self, token):
        token.board_sensor = tiledboardsensor.TokenTiledBoardSensor(token, self.board)
        token._managers.append(token.board_sensor)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = hexpositionmanager.HexBoardPositionManager(token, position)
        token._managers.append(token.position_manager)

    def remove_token_from_board(self, token):
        """
        Implemented in subclasses
        """
        self.remove_static_token()
        self.remove_dynamic_token()
        super().remove_token_from_board(token)


    def add_board_costume_manager_to_token(self, token):
        token._costume = hex_costume.HexCostume(token)
        token.costume_manager = costumes_manager.CostumesManager(token, token._costume)
        token._managers.append(token.costume_manager)