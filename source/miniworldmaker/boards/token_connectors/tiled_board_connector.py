from miniworldmaker.tokens.sensors import token_tiledboardsensor as tiledboardsensor
from miniworldmaker.tokens.positions import token_tiled_position_manager as tiledpositionmanager
from miniworldmaker.boards.token_connectors import token_connector as token_connector
from miniworldmaker.board_positions import board_position as board_position


class TiledBoardConnector(token_connector.TokenConnector):
    def add_token_to_board(self, position: "board_position.Position"):
        super().add_token_to_board(position)
        # self.token.costume_manager.set_size()

    def add_board_sensor_to_token(self, token):
        token.board_sensor = tiledboardsensor.TokenTiledBoardSensor(token, self.board)
        token._managers.append(token.board_sensor)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = tiledpositionmanager.TiledBoardPositionManager(token, position)
        token._managers.append(token.position_manager)

    def remove_token_from_board(self, token):
        """
        Implemented in subclasses
        """
        self.remove_static_token()
        self.remove_dynamic_token()
        super().remove_token_from_board(token)

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
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.add_static_token()
        else:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.remove_static_token()
