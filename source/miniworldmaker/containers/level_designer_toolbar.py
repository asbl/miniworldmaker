from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *
import miniworldmaker.tokens.board_token as token
import miniworldmaker.boards.board_position as board_position
import os


class LevelDesignerToolbar(toolbar.Toolbar):

    def __init__(self, board):
        super().__init__()
        self.default_size = 400
        self.board = board
        self.selected_token_type = None
        self.register_events.add("all")
        self.register_events.add("debug")
        self.add_widget(ToolbarLabel("Left Click to add Tokens"))
        self.add_widget(ToolbarLabel("Right Click or Wheel to change direction"))
        self.add_widget(ToolbarLabel("SHIFT + Right Click to delete token"))
        class_list = self.all_subclasses(token.Token)
        for cls in class_list:
            self.add_widget(TokenButton(cls, board, self))

        db_file = "data.db"

        self.add_widget(SaveButton(board = self.board, text = "Save", filename=db_file))
        if os.path.exists(db_file):
            self.add_widget(LoadButton(board = self.board, text = "Load", filename=db_file ))
        self.board.is_running = False

    def all_subclasses(self, cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in self.all_subclasses(c)])

    def get_event(self, event, data):
        super().get_event(event, data)
        if self.selected_token_type:
            if "mouse_left" in event:
                print("ml")
                if self.board.is_in_container(data[0], data[1]):
                    print("in container")
                    keys = self.board.window.get_keys()
                    if "L_SHIFT" in keys:
                        for i in range(self.board.rows):
                            for j in range(self.board.columns):
                                self.selected_token_type((j, i))
                    else:
                        self.selected_token_type(position=board_position.BoardPosition.from_pixel(data))

            elif "wheel_up" in event or "wheel_down" in event:
                if self.board.is_in_container(data[0], data[1]):
                    token = self.board.get_token(data)
                    for cls in token.__class__.__mro__:
                        if cls.__name__ == "Actor":
                            if event == "wheel_up":
                                token.turn_left(5)
                            elif event == "wheel_down":
                                token.turn_right(5)
            elif "mouse_motion" in event:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.board.is_in_container(data[0], data[1]):
                        token = self.board.get_token(data)
                        if token.__class__ != self.selected_token_type:
                            token = self.selected_token_type(position=board_position.BoardPosition.from_pixel(data))
        if "mouse_right" in event:
            if self.board.is_in_container(data[0], data[1]):
                keys = self.board.window.get_keys()
                if "L_SHIFT" in keys:
                    token = self.board.get_token(data)
                    while token != None:
                        if token:
                            token.remove()
                        token = self.board.get_token(data)
                else:
                    token = self.board.get_token(data)
                    for cls in token.__class__.__mro__:
                        if cls.__name__ == "Actor":
                            token.turn_left(5)




class TokenButton(ToolbarWidget):

    def __init__(self, token_type, board, parent):
        super().__init__()
        self.parent = parent
        self.board = board
        token = token_type(position = None)
        if token.costume.image_paths != []:
            self._img_path = token.costume.image_paths[0]
        self._text_padding = 30
        self.set_text("Add " + token_type.__name__)
        self.token_type = token_type
        self.background_color = (180,180,180, 255)

    def get_event(self, event, data):
        if event == "mouse_left":
            self.parent.window.send_event_to_containers("Selected actor", self.token_type)
            self.parent.selected_token_type = self.token_type
            for widget in self.parent.widgets:
                if widget.__class__ == TokenButton:
                    widget.background_color = (180, 180, 180, 255)
                    widget.dirty = 1
            self.background_color = (100, 100, 100, 255)
            self.dirty = 1
