import abc

from miniworldmaker.appearances import costume
from miniworldmaker.appearances import costumes_manager
from miniworldmaker.boards.board_templates.pixel_board import board as board_mod
from miniworldmaker.tokens import token as token_mod
from miniworldmaker.tokens.managers import token_event_manager
from miniworldmaker.tokens.managers import token_position_manager, token_boardsensor


class TokenConnector(abc.ABC):
    def __init__(self, board: "board_mod.Board", token: "token_mod.Token"):
        self.board: "board_mod.Board" = board
        self.token: "token_mod.Token" = token
        self._costume = None
        self._costume_manager = None
        self._board_sensor: "token_boardsensor.TokenBoardSensor" = None
        self._position_manager: "token_position_manager.TokenPositionManager" = None

    def create_board_sensor(self) -> "token_boardsensor.TokenBoardSensor":
        return self.get_board_sensor_class()(self.token, self.board)

    def create_position_manager(self) -> "token_position_manager.TokenPositionManager":
        return self.get_position_manager_class()(self.token, self.board)

    def create_costume(self) -> "costume.Costume":
        return self._get_token_costume_class()(self.token)

    def create_costume_manager(self) -> "costumes_manager.CostumesManager":
        return self._get_token_costume_manager_class()(self.token)

    def create_event_manager(self):
        return self._get_token_event_manager_class()(self.token)

    @staticmethod
    def _get_token_event_manager_class():
        return token_event_manager.TokenEventManager

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

    def add_token_to_board(self):
        if self.board.is_display_initialized:
            self.token.is_display_initialized = True
        self.board.camera.clear_camera_cache()
        self.board.tokens.add(self.token)
        self.set_static(self.token.static)
        self.token.costume.set_dirty("all", costume.Costume.LOAD_NEW_IMAGE)
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
            self.board.background.reload_costumes_queue.append(self.token)
        self.board.event_manager.register_events_for_token(self.token)

    def remove_token_from_board(self, token):
        self.board.camera.clear_camera_cache()
        self.board.event_manager.unregister_instance(token)
        if self in self.board.background.reload_costumes_queue:
            self.board.background.reload_costumes_queue.remove(self)
        if not self.token._static:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.remove_dynamic_token()
        self.board.tokens.remove(token)
        for colliding_token in token.detect_tokens():
            colliding_token.dirty = 1
        for manager in token._managers:
            manager.self_remove()
            del manager
        token.kill()
        del (token)

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
