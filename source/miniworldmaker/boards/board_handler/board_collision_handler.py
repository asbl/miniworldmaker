from miniworldmaker.tools import method_caller


class BoardCollisionHandler:
    def __init__(self, board):
        self.board = board

    def handle_all_collisions(self):
        self._handle_token_sensing_token_methods()
        self._handle_token_not_sensing_token_methods()
        self._handle_token_sensing_border_methods()
        self._handle_token_sensing_on_board_methods()
        self._handle_token_sensing_not_on_board_methods()

    def _handle_token_sensing_token_methods(self):
        for method in self.board.event_handler.registered_events["on_sensing_token"].copy():
            token = method.__self__
            token_type_of_target = method.__name__[11:]
            found_tokens_for_token_type = token.sensing_tokens(token_filter=token_type_of_target)
            if found_tokens_for_token_type == None: # found nothing
                found_tokens_for_token_type = []
            if token in found_tokens_for_token_type: # found self
                found_tokens_for_token_type.remove(token)
            for found_token in found_tokens_for_token_type: # found other token
                if found_token.__class__.__name__.lower() == token_type_of_target:
                    method_caller.call_method(method, [found_token])

    def _handle_token_not_sensing_token_methods(self):
        for method in self.board.event_handler.registered_events["on_not_sensing_token"].copy():
            token = method.__self__
            token_type_of_target = method.__name__[15:]
            found_tokens_for_token_type = token.sensing_tokens(token_filter=token_type_of_target)
            if found_tokens_for_token_type == None:
                found_tokens_for_token_type = []
                method_caller.call_method(method, None)
                return
            if token in found_tokens_for_token_type:
                found_tokens_for_token_type.remove(token)
            for found_token in found_tokens_for_token_type:
                if found_token.__class__.__name__.lower() == token_type_of_target:
                    return
            method_caller.call_method(method, None)


    def _handle_token_sensing_border_methods(self):
        for event in self.board.event_handler.border_events:
            for method in self.board.event_handler.registered_events[event]:
                sensed_borders = method.__self__.sensing_borders()
                if method.__name__ == "on_sensing_borders" and sensed_borders:
                    method_caller.call_method(
                        method, [sensed_borders])
                else:
                    self._handle_token_sensing_specific_border_methods(method, sensed_borders)

    def _handle_token_sensing_specific_border_methods(self, method, sensed_borders):
        for border in sensed_borders:
            if border in method.__name__:
                method_caller.call_method(method, None)

    def _handle_token_sensing_on_board_methods(self):
        for method in self.board.event_handler.registered_events["on_sensing_on_board"].copy():
            is_on_board = method.__self__.sensing_on_board()
            if is_on_board:
                method_caller.call_method(method, None)

    def _handle_token_sensing_not_on_board_methods(self):
        for method in self.board.event_handler.registered_events["on_sensing_not_on_board"].copy():
            is_not_on_board = not method.__self__.sensing_on_board()
            if is_not_on_board:
                method_caller.call_method(method, None)
