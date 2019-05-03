from miniworldmaker.containers.toolbar import Toolbar
from miniworldmaker.containers.toolbar_widgets import *


class SelectTokenTypeToolbar(Toolbar):
    def __init__(self, board):
        super().__init__()
        self.board = board
        for token_type in board.registered_token_types:
            self.add_widget(ActorButton(token_type, board, self))
        self.selected_actor = board.registered_token_types[list(board.registered_token_types.keys())[0]]


class ActorButton(ToolbarWidget):

    def __init__(self, token_type, board, parent):
        super().__init__()
        self.parent = parent
        self.board = board
        token = self.board.registered_token_types[token_type](position = None)
        self._img_path = token.costume.image_paths[0]
        self._text_padding = 30
        self.set_text(token_type)
        self.token_type = token_type

    def get_event(self, event, data):
        if event == "mouse_left":
            self.parent.window.send_event_to_containers("Selected actor", self.token_type)
            self.parent.selected_actor = self.board.registered_token_types[self.token_type]
