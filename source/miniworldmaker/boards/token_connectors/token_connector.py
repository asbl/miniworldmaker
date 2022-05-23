from miniworldmaker.appearances import costumes_manager
from miniworldmaker.appearances import costume


class TokenConnector:
    def __init__(self, board, token):
        self.board = board
        self.token = token
        self.board_sensor = None
        self.position_manager = None

    def get_board_sensor(self, position):
        return None

    @staticmethod
    def get_position_manager_class(self):
        return None

    def add_token_managers(self, position):
        self.add_position_manager_to_token(self.token, position)
        self.add_board_costume_manager_to_token(self.token)
        self.add_board_sensor_to_token(self.token)

    def add_token_to_board(self, position):
        self.board.tokens.add(self.token)
        self.set_static(self.token.static)
        self.token.costume.reload_transformations_after("all")
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
            self.board.background.reload_costumes_queue.append(self.token)
        if not self.token.static:
            self.token.board.event_manager.register_events_for_token(self.token)

    def add_position_manager_to_token(self, token, position):
        token.position_manager = self.get_position_manager_class()(token, position)
        token._managers.append(token.position_manager)
        
    def add_board_sensor_to_token(self, token):
        token.board_sensor = self.board_sensor
        token._managers.append(token.board_sensor)

    def add_board_costume_manager_to_token(self, token):
        token._costume = costume.Costume(token)
        token.costume_manager = costumes_manager.CostumesManager(token, token._costume)
        token._managers.append(token.costume_manager)

    def remove_token_from_board(self, token):
        """
        Implemented in subclasses
        """
        self.board.event_manager.unregister_instance(token)
        if self in self.board.background.reload_costumes_queue:
            self.board.background.reload_costumes_queue.remove(self)
        if not self.token._static:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.remove_dynamic_token()
        self.board.tokens.remove(token)

    def set_static(self, value):
        self.token._static = value
        if self.token._static:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.remove_dynamic_token()
        else:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.add_dynamic_token()

    def remove_dynamic_token(self):
        if self.token in self.board.dynamic_tokens:
            self.board.dynamic_tokens.remove(self.token)

    def add_dynamic_token(self):
        if self.token not in self.board.dynamic_tokens:
            self.board.dynamic_tokens.add(self.token)
