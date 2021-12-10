class TokenConnector:

    def __init__(self, board, token):
        self.board = board
        self.token = token

    def add_token_managers(self, image, position):
        self.add_board_costume_manager_to_token(self.token, image)
        self.add_position_manager_to_token(self.token, position)
        self.add_board_sensor_to_token(self.token)

    def add_token_to_board(self, position):
        self.board.tokens.add(self.token)
        self.token.dirty = 1
        if self.token.costume:
            self.token.costume._reload_all()
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
        if not self.token.static:
            self.token.board.event_handler.register_events_for_token(self.token)

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
        self.board.event_handler.unregister_instance(token)
        self.board.tokens.remove(token)
