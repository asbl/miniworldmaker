from collections import defaultdict
import inspect
from miniworldmaker.tools.inspection_methods import InspectionMethods


class BoardCollisionHandler:
    def __init__(self, board):
        self.board = board
        self.tokens_with_collisionhandler: defaultdict = defaultdict(list)

    def handle_all_collisions(self):
        for token in self.board.tokens:
            self._handle_collision_with_tokens(token)
            self._handle_collision_with_borders(token)
            self._handle_on_board(token)

    def _get_magic_methods(self, token):
        border_methods_dict = {"on_sensing_left_border": InspectionMethods.get_instance_method(token, "on_sensing_left_border"),
                               "on_sensing_right_border": InspectionMethods.get_instance_method(token, "on_sensing_right_border"),
                               "on_sensing_bottom_border": InspectionMethods.get_instance_method(token, "on_sensing_bottom_border"),
                               "on_sensing_top_border": InspectionMethods.get_instance_method(token, "on_sensing_top_border"),
                               "on_sensing_on_board": InspectionMethods.get_instance_method(token, 'on_sensing_on_board'.lower()),
                               "on_sensing_not_on_board": InspectionMethods.get_instance_method(token, 'on_sensing_not_on_board'.lower()),
                               "on_sensing_borders":InspectionMethods.get_instance_method(token, "on_sensing_borders")
                               }
        return border_methods_dict

    def _handle_collision_with_token(self, token, other_token):
        parents = inspect.getmro(other_token.__class__)
        other_and_parents = list(parents)
        if other_and_parents:
            for other_class in other_and_parents:
                method_name = ('on_sensing_' + str(other_class.__name__)).lower()
                method = InspectionMethods.get_instance_method(token, method_name)
                if method:
                    InspectionMethods.call_instance_method(token, method, [other_token])

    def _handle_collision_with_tokens(self, token):
        members = dir(token)
        found_tokens = []
        for token_type in [member[11:] for member in members if member.startswith("on_sensing_") and member not in self._get_magic_methods(token).keys()]:
            tokens_for_token_type = token.sensing_tokens(token_type=token_type.capitalize())
            if tokens_for_token_type:
                for found_token in tokens_for_token_type:
                    if found_token not in found_tokens:
                        found_tokens.append(found_token)
                        self._handle_collision_with_token(token, found_token)
                

    def _handle_collision_with_borders(self, token):
        border_methods_dict = {"on_sensing_left_border": InspectionMethods.get_instance_method(token, "on_sensing_left_border"),
                               "on_sensing_right_border": InspectionMethods.get_instance_method(token, "on_sensing_right_border"),
                               "on_sensing_bottom_border": InspectionMethods.get_instance_method(token, "on_sensing_bottom_border"),
                               "on_sensing_top_border": InspectionMethods.get_instance_method(token, "on_sensing_top_border"),
                               }
        on_sensing_borders = InspectionMethods.get_instance_method(token, "on_sensing_borders")
        if on_sensing_borders or [method for method in border_methods_dict.values() if method is not None]:
            sensed_borders = token.sensing_borders()
            if sensed_borders:
                if on_sensing_borders:
                    InspectionMethods.call_instance_method(
                        token, on_sensing_borders, [sensed_borders])
                for key in border_methods_dict.keys():
                    if border_methods_dict[key]:
                        for border in sensed_borders:
                            if border in key:
                                InspectionMethods.call_instance_method(
                                    token, border_methods_dict[key], None)

    def _handle_on_board(self, a_object):
        on_board_handler = InspectionMethods.get_instance_method(
            a_object, 'on_sensing_on_board'.lower())
        not_on_board_handler = InspectionMethods.get_instance_method(
            a_object, 'on_sensing_not_on_board'.lower())
        if on_board_handler or not_on_board_handler:
            is_on_board = a_object.sensing_on_board()
            if is_on_board:
                if on_board_handler:
                    on_board_handler()
            else:
                if not_on_board_handler:
                    not_on_board_handler()
