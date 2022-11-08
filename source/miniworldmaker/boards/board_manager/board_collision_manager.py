import miniworldmaker.tools.method_caller as method_caller
import miniworldmaker.tools.token_class_inspection as token_class_inspection


class BoardCollisionManager:
    """The class handles all collisions of tokens.

    The method ``handle_all_collisions`` is called every frame (in BaseBoard.update())
    """

    def __init__(self, board):
        self.board = board

    def handle_all_collisions(self):
        self._handle_token_detecting_token_methods()
        self._handle_token_not_detecting_token_methods()
        self._handle_token_detecting_border_methods()
        self._handle_token_detecting_on_the_board_methods()
        self._handle_token_detecting_not_on_the_board_methods()

    def _handle_on_detecting_all_tokens(self, token, method):
        found_tokens_for_token_type = token.board_sensor.detect_tokens(token_filter=None)
        if not found_tokens_for_token_type:  # found nothing
            found_tokens_for_token_type = []
        if token in found_tokens_for_token_type:  # found self
            found_tokens_for_token_type.remove(token)
        for found_token in found_tokens_for_token_type:  # found other token
            method_caller.call_method(method, found_token, found_token.__class__)

    def _handle_on_detetecting_tokens_by_filter(self, token, method, token_filter):
        found_tokens_for_token_type = token.board_sensor.detect_tokens(token_filter=token_filter)
        if not found_tokens_for_token_type:  # found nothing
            found_tokens_for_token_type = []
        if token in found_tokens_for_token_type:  # found self
            found_tokens_for_token_type.remove(token)
        for found_token in found_tokens_for_token_type:  # found other token
            subclasses = token_class_inspection.TokenClassInspection.get_all_token_classes()
            if found_token.__class__ in subclasses:
                method_caller.call_method(method, found_token, found_token.__class__)

    def _handle_token_detecting_token_methods(self):
        for event in self.board.event_manager.class_events["on_detecting"]:
            registered_events_copy = list(self.board.event_manager.registered_events[event].copy())
            for method in registered_events_copy:
                token = method.__self__
                if method.__name__ == "on_detecting":
                    self._handle_on_detecting_all_tokens(token, method)
                    return
                elif len(method.__name__.split("_")) != 3:
                    return
                else:
                    token_filter = method.__name__.split("_")[2]
                self._handle_on_detetecting_tokens_by_filter(token, method, token_filter)
            del registered_events_copy

    def _handle_token_not_detecting_token_methods(self):
        for event in self.board.event_manager.class_events["on_not_detecting"]:  # first level
            for method in self.board.event_manager.registered_events[event].copy():  # concrete method
                token = method.__self__
                if len(method.__name__.split("_")) != 4:
                    return
                else:
                    token_type_of_target = method.__name__.split("_")[3]
                found_tokens_for_token_type = token.detect_tokens(token_filter=token_type_of_target)
                if found_tokens_for_token_type:
                    method_caller.call_method(method, None)
                    return
                if token in found_tokens_for_token_type:
                    found_tokens_for_token_type.remove(token)
                for found_token in found_tokens_for_token_type:
                    subclasses = token_class_inspection.TokenClassInspection(token).get_all_token_classes()
                    if found_token.__class__ in subclasses:
                        return
                method_caller.call_method(method, None)

    def _handle_token_detecting_border_methods(self):
        for event in self.board.event_manager.class_events["border"]:
            for method in self.board.event_manager.registered_events[event]:
                sensed_borders = method.__self__.detect_borders()
                if method.__name__ == "on_detecting_borders" and sensed_borders:
                    method_caller.call_method(
                        method, (sensed_borders,))
                else:
                    self._handle_token_sensing_specific_border_methods(method, sensed_borders)

    def _handle_token_sensing_specific_border_methods(self, method, sensed_borders):
        for border in sensed_borders:
            if border in method.__name__:
                method_caller.call_method(method, None)

    def _handle_token_detecting_on_the_board_methods(self):
        methods = self.board.event_manager.registered_events["on_detecting_board"].copy().union(
            self.board.event_manager.registered_events["on_detecting_board"].copy())
        for method in methods:
            is_on_the_board = method.__self__.is_detecting_board()
            if is_on_the_board:
                method_caller.call_method(method, None)
        del methods

    def _handle_token_detecting_not_on_the_board_methods(self):
        methods = self.board.event_manager.registered_events["on_sensing_not_on_board"].copy().union(
            self.board.event_manager.registered_events["on_not_detecting_board"].copy())
        for method in methods:
            is_not_on_the_board = not method.__self__.is_detecting_board()
            if is_not_on_the_board:
                method_caller.call_method(method, None)
        del methods
