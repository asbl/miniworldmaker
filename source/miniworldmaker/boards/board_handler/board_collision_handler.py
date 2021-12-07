from collections import defaultdict
import inspect
from miniworldmaker.tools import inspection_methods


class BoardCollisionHandler:
    def __init__(self, board):
        self.board = board

    def handle_all_collisions(self):
        self._handle_collision_with_tokens()
        self._handle_collision_with_borders()
        self._handle_on_board()
        self._handle_not_on_board()

    def _handle_collision_with_tokens(self):
        for method in self.board.event_handler.registered_events["on_sensing_token"].copy():
            token = method.__self__
            searched_token_type = method.__name__[11:]
            found_tokens_for_token_type = token.sensing_tokens(token_filter=searched_token_type)
            if found_tokens_for_token_type == None:
                found_tokens_for_token_type = []
            if token in found_tokens_for_token_type:
                found_tokens_for_token_type.remove(token)
            for found_token in found_tokens_for_token_type:
                if found_token.__class__.__name__.lower() == searched_token_type:
                    inspection_methods.InspectionMethods.call_method(method, [found_token])

    def _handle_collision_with_borders(self):
        for event in self.board.event_handler.border_events:
            for method in self.board.event_handler.registered_events[event]:
                sensed_borders = method.__self__.sensing_borders()
                if method.__name__ == "on_sensing_borders" and sensed_borders:
                    inspection_methods.InspectionMethods.call_method(
                        method, [sensed_borders])
                else:
                    self._handle_specific_border(method, sensed_borders)

    def _handle_specific_border(self, method, sensed_borders):
        for border in sensed_borders:
            if border in method.__name__:
                inspection_methods.InspectionMethods.call_method(
                    method, None)

    def _handle_on_board(self):
        for method in self.board.event_handler.registered_events["on_sensing_on_board"].copy():
            is_on_board = method.__self__.sensing_on_board()
            if is_on_board:
                inspection_methods.InspectionMethods.call_method(
                    method, None)

    def _handle_not_on_board(self):
        for method in self.board.event_handler.registered_events["on_sensing_not_on_board"].copy():
            is_not_on_board = not method.__self__.sensing_on_board()
            if is_not_on_board:
                inspection_methods.InspectionMethods.call_method(
                    method, None)
