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
        self.token.fill_color = self.board.fill_color
        self.token.border_color = self.board.stroke_color
        self.token.costume_manager.reload_costume()
        self.token.dirty = 1
        if self.token.costume:
            self.token.costume._reload_all()
        if hasattr(self.token, "on_setup"):
            self.token.on_setup()
            self.board.view_handler.reload_costumes_queue.append(self.token)
        if not self.token.static:
            self.token.board.event_handler.register_events_for_token(self.token)
        self.token.color = self.board.fill_color

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
        if self in self.board.view_handler.reload_costumes_queue:
            self.board.view_handler.reload_costumes_queue.remove(self)
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
        self.board.dynamic_tokens.add(self.token)
