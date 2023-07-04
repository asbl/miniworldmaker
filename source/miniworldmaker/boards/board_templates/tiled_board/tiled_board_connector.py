from miniworldmaker.boards.board_templates.tiled_board import token_tiled_position_manager as tiledpositionmanager, \
    token_tiledboardsensor as tiledboardsensor
from miniworldmaker.boards.token_connectors import token_connector as token_connector


class TiledBoardConnector(token_connector.TokenConnector):

    def __init__(self, board, token):
        super().__init__(board, token)

    @staticmethod        
    def get_board_sensor_class():
        return tiledboardsensor.TokenTiledBoardSensor
    
    @staticmethod
    def get_position_manager_class():
        return tiledpositionmanager.TiledBoardPositionManager

    def remove_token_from_board(self):
        self.remove_static_token()
        self.remove_dynamic_token()
        super().remove_token_from_board()

    def add_static_token(self):
        if self.token not in self.board.static_tokens_dict[self.token.position]:
            self.board.static_tokens_dict[self.token.position].append(self.token)
            self.board.background.reload_costumes_queue.append(self.token)

    def remove_static_token(self):
        if (
            self.token.position in self.board.static_tokens_dict
            and self.token in self.board.static_tokens_dict[self.token.position]
        ):
            self.board.static_tokens_dict[self.token.position].remove(self.token)

    def set_static(self, value):
        super().set_static(value)
        if self.token._static:
            self.add_static_token()
        else:
            self.remove_static_token()
