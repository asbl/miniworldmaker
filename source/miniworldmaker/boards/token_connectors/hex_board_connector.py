import miniworldmaker.appearances.hex_costume as hex_costume
import miniworldmaker.appearances.costumes_manager as costumes_manager
import miniworldmaker.tokens.sensors.token_tiledboardsensor as tiledboardsensor
import miniworldmaker.tokens.positions.token_hex_position_manager as hexpositionmanager
import miniworldmaker.boards.token_connectors.tiled_board_connector as tiled_board_connector


class HexBoardConnector(tiled_board_connector.TiledBoardConnector):
    def __init__(self, board, token):
        super().__init__(board, token)

    @staticmethod
    def get_position_manager_class():
        return hexpositionmanager.HexBoardPositionManager

    @staticmethod
    def _get_token_costume_class():
        return hex_costume.HexCostume

    @staticmethod
    def _get_token_costume_manager_class():
        return costumes_manager.CostumesManager
