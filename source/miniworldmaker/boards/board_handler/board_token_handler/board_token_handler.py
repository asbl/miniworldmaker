import pygame
from collections import defaultdict
import miniworldmaker.inspection_methods
import miniworldmaker.tokens.sensors.token_tiledboardsensor as tiledboardsensor


class BoardTokenHandler:

    def __init__(self, board):
        self.board = board
        self.tokens: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()

    def update_all_costumes(self):
        [token.costume.update() for token in self.tokens]

    def act_all(self):
        for token in self.tokens:
            if token.board:  # is on board
                self.board.event_handler.handle_act_event(token)
        # If board has act method call board.act()
        method = miniworldmaker.inspection_methods.InspectionMethods.get_instance_method(
            self.board, "act")
        if method:
            method = miniworldmaker.inspection_methods.InspectionMethods.call_instance_method(
                self.board, method, None)

    def add_token_managers(self, token, image, position):
        self.add_board_costume_manager_to_token(token, image)
        self.add_position_manager_to_token(token, position)
        self.add_board_sensor_to_token(token)

    def add_token_to_board(self, token, position):
        self.tokens.add(token)
        token.dirty = 1
        if token.is_setup != 1:
            raise UnboundLocalError("super().__init__() was not called")

    def add_position_manager_to_token(self, token, position):
        """
        Implemented in subclasses
        """
        pass

    def add_board_sensor_to_token(self, token):
        """
        Implemented in subclasses
        """
        pass

    def add_board_costume_manager_to_token(self, token, image):
        """
        Implemented in subclasses
        """
        pass

    def remove_token_from_board(self, token):
        """
        Implemented in subclasses
        """
        pass

    def clean(self):
        for token in self.tokens:
            token.remove()
            del(token)

    def register_token_method(self, token, method: callable):
        bound_method = method.__get__(token, token.__class__)
        setattr(token, method.__name__, bound_method)
        if method.__name__ == "on_setup":
            token.on_setup()
        return bound_method
