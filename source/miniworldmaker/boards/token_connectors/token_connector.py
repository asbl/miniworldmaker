from miniworldmaker.appearances import costumes_manager
from miniworldmaker.appearances import costume
from miniworldmaker.tokens.positions import token_position_manager
from miniworldmaker.tokens.sensors import token_boardsensor
from miniworldmaker.tokens import token
from miniworldmaker.boards import board

class TokenConnector:
    def __init__(self, board : "board.Board", token : "token.Token"):
        self.board : "board.Board" = board
        self.token : "token.Token" = token
        self._costume = None
        self._costume_manager = None
        self._board_sensor : "token_boardsensor.TokenBoardSensor" = None
        self._position_manager : "token_position_manager.TokenPositionManager" = None

    def create_board_sensor(self) -> "token_boardsensor.TokenBoardSensor":
        return self.get_board_sensor_class()(self.token, self.board)
            
    def create_position_manager(self) -> "token_position_manager.TokenPositionManager" :
        return self.get_position_manager_class()(self.token, self.board)

    def create_costume(self) -> "costume.Costume":
        return self._get_token_costume_class()(self.token)
                
    def create_costume_manager(self) -> "costumes_manager.CostumesManager":
        return self._get_token_costume_manager_class()(self.token)
 
    @staticmethod
    def _get_token_costume_manager_class():
        return costumes_manager.CostumesManager

    @staticmethod
    def _get_token_costume_class():
        return costume.Costume
               
                              
    @staticmethod
    def get_position_manager_class():
        return None

    @staticmethod
    def get_board_sensor_class():
        return None

    def add_token_to_board(self, position):
        self.board.tokens.add(self.token)
        self.set_static(self.token.static)
        self.token.costume.reload_transformations_after("all")
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
            self.board.background.reload_costumes_queue.append(self.token)
        if not self.token.static:
            self.token.board.event_manager.register_events_for_token(self.token)
      
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
