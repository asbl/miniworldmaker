import miniworldmaker.appearances.hex_costume as hex_costume
import miniworldmaker.appearances.costumes_manager as costumes_manager
import miniworldmaker.tokens.sensors.token_tiledboardsensor as tiledboardsensor
import miniworldmaker.tokens.positions.token_hex_position_manager as hexpositionmanager
import miniworldmaker.boards.token_connectors.tiled_board_connector as tiled_board_connector


class HexBoardConnector(tiled_board_connector.TiledBoardConnector):

    def __init__(self, board, token):
        super().__init__(board, token)

    def get_position_manager_class(self):
        return hexpositionmanager.HexBoardPositionManager

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
