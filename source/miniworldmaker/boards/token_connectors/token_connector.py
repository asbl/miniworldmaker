import collections
from abc import abstractmethod, ABC
from typing import Optional, Dict
from typing import Type

from miniworldmaker.appearances import costume
from miniworldmaker.appearances import costumes_manager
from miniworldmaker.boards.board_templates.pixel_board import board as board_mod
from miniworldmaker.tokens import token as token_mod
from miniworldmaker.tokens.managers import token_position_manager, token_boardsensor


class TokenConnector(ABC):
    def __init__(self, board: "board_mod.Board", token: "token_mod.Token"):
        self.board: "board_mod.Board" = board
        self.token: "token_mod.Token" = token
        self._costume = None
        self._costume_manager = None
        self._board_sensor: Optional["token_boardsensor.TokenBoardSensor"] = None
        self._position_manager: Optional["token_position_manager.TokenPositionManager"] = None

    def create_board_sensor(self) -> "token_boardsensor.TokenBoardSensor":
        return self.get_board_sensor_class()(self.token, self.board)

    def create_position_manager(self) -> "token_position_manager.TokenPositionManager":
        return self.get_position_manager_class()(self.token, self.board)

    def create_costume(self) -> "costume.Costume":
        token_costume_class = self.token.get_costume_class()
        if not token_costume_class:
            return self.get_token_costume_class()(self.token)
        else:
            return token_costume_class(self.token)

    @staticmethod
    def get_token_costume_class() -> Type["costume.Costume"]:
        return costume.Costume

    def create_costume_manager(self) -> "costumes_manager.CostumesManager":
        return self._get_token_costume_manager_class()(self.token)

    @staticmethod
    def _get_token_costume_manager_class():
        return costumes_manager.CostumesManager



    @staticmethod
    @abstractmethod
    def get_position_manager_class() -> Type["token_position_manager.TokenPositionManager"]:
        pass

    @staticmethod
    @abstractmethod
    def get_board_sensor_class() -> Type["token_boardsensor.TokenBoardSensor"]:
        pass

    def init_managers(self, position):
        if not self.token._has_board_sensor:
            self.init_board_sensor()
            self.token._has_board_sensor = True
        if not self.token._has_position_manager:
            self.init_position_manager(position)
            self.token._has_position_manager = True
        if not self.token._has_costume_manager:
            self.init_costume_manager()
            self.token._has_costume_manager = True

    def add_token_to_board(self):
        if self.board.is_display_initialized:
            self.token.is_display_initialized = True
        self.init_managers(self.token._position)
        self.board.camera.clear_camera_cache()
        self.board.tokens.add(self.token)
        self.set_static(self.token.static)
        if self.token.costume:
            self.token.costume.set_dirty("all", costume.Costume.LOAD_NEW_IMAGE)
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
            self.board.background.reload_costumes_queue.append(self.token)
        self.board.event_manager.register_events_for_token(self.token)

    def remove_token_from_board(self) -> collections.defaultdict:
        """
        Removes a token from board

        Returns:unregistered methods from event handler.
        """
        self.token._is_acting = False
        self.board.camera.clear_camera_cache()
        unregistered_methods = self.board.event_manager.unregister_instance(self.token)
        if self in self.board.background.reload_costumes_queue:
            self.board.background.reload_costumes_queue.remove(self)
        if not self.token._static:
            _token_connector = self.board.get_token_connector(self.token)
            _token_connector.remove_dynamic_token()
        self.board.tokens.remove(self.token)
        for colliding_token in self.token.detect_tokens():
            colliding_token.dirty = 1
        self.token._board_sensor.remove_from_board()
        self.token._board_sensor = None
        self.token._has_board_sensor = False
        del self.token._board_sensor
        self.token._position_manager.remove_from_board()
        self.token._position_manager = None
        self.token._has_position_manager = False
        del self.token._position_manager
        return unregistered_methods

    def switch_board(self, new_board):
        # Store some old values, which should be transported
        old_connector = self.token.board.get_token_connector(self.token)
        sticky = self.token.sticky
        unregistered_methods = old_connector.remove_token_from_board()
        new_connector = new_board.get_token_connector(self.token)
        new_connector.add_token_to_board()
        new_connector.token._board = new_board
        new_connector.register_event_methods(unregistered_methods)
        self.token.sticky = sticky

    def register_event_methods(self, method_dict: Dict[str, callable]):
        if method_dict:
            for event, method in method_dict.items():
                self.token.register(method)

    def init_board_sensor(self):
        self.token._board_sensor = self.create_board_sensor()
        return self.token._board_sensor

    def init_position_manager(self, position=(0, 0)):
        self.token._position_manager = self.create_position_manager()
        self.token._position_manager.position = position
        return self.token._position_manager

    def init_costume_manager(self):
        self.token._costume_manager = self.create_costume_manager()
        self.token._costume_manager._add_default_appearance()
        return self.token._costume_manager

    def delete_token(self):
        if not self.token._is_deleted:
            self.token._is_deleted = True
            self.remove_token_from_board()
            self.token._costume_manager.remove_from_board()
            self.token._costume_manager = None
            self.token._has_costume_manager = False
            del self.token._costume_manager
            self.token.kill()
            del self.token

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
