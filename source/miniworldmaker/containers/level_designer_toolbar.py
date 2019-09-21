import os

from miniworldmaker.board_positions import board_position
from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *


class LevelDesignerToolbar(toolbar.Toolbar):

    def __init__(self, board):
        super().__init__()
        self.default_size = 400
        self.board = board
        self.selected_token_type = None
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.add_widget(ToolbarLabel("Left Click to add Tokens"))
        self.add_widget(ToolbarLabel("Right Click or Wheel to change direction"))
        self.add_widget(ToolbarLabel("SHIFT + Right Click to delete token"))
        import miniworldmaker.tokens.token as tk
        class_set = self.all_subclasses(tk.Token)
        excluded = ["Token",
                    "Actor",
                    "TextToken",
                    "NumberToken",
                    "Circle",
                    "Line",
                    "Ellipse",
                    "Polygon",
                    "Rectangle",
                    "Shape",
                    "TiledBoardToken",
                    "PixelBoardToken",
                    "Point",
                    ]
        [self.add_widget(TokenButton(cls, board, self)) for cls in class_set if cls.__name__ not in excluded]
        db_file = "data.db"
        self.add_widget(SaveButton(board=self.board, text="Save", filename=db_file))
        if os.path.exists(db_file):
            self.add_widget(LoadButton(board=self.board, text="Load", filename=db_file))
        self.board.is_running = False

    def all_subclasses(self, parent_cls) -> set:
        return set(parent_cls.__subclasses__()).union(
            [s for c in parent_cls.__subclasses__() for s in self.all_subclasses(c)])

    def get_event(self, event, data):
        super().get_event(event, data)
        if self.selected_token_type:
            if "mouse_left" in event:
                if self.board.is_in_container(data[0], data[1]):
                    keys = self.board.window.get_keys()
                    if "L_SHIFT" in keys:
                        for i in range(self.board.rows):
                            for j in range(self.board.columns):
                                self.selected_token_type((j, i))
                    else:
                        try:
                            import miniworldmaker.board_positions.board_position as bp
                            self.selected_token_type(position=bp.BoardPosition.from_pixel(data))
                        except TypeError:
                            print("Can't create tokens with more than one parameter position yet")

            elif "wheel_up" in event or "wheel_down" in event:
                if self.board.is_in_container(data[0], data[1]):
                    token = self.board.get_token_in_area(data)
                    for cls in token.__class__.__mro__:
                        if cls.__name__ == "Actor":
                            if event == "wheel_up":
                                token.turn_left(5)
                            elif event == "wheel_down":
                                token.turn_right(5)
            elif "mouse_motion" in event:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.board.is_in_container(data[0], data[1]):
                        rect = board_position.BoardPosition(data[0], data[1]).to_rect()
                        token = self.board.get_tokens_at_rect(rect, singleitem=True)
                        if token.__class__ != self.selected_token_type:
                            import miniworldmaker.board_positions.board_position as bp
                            token = self.selected_token_type(position=bp.BoardPosition.from_pixel(data))
        if "mouse_right" in event:
            if self.board.is_in_container(data[0], data[1]):
                keys = self.board.window.get_keys()
                if "L_SHIFT" in keys:
                    tokens = self.board.get_tokens_by_pixel(data)
                    while tokens:
                        token = tokens.pop()
                        token.remove()
                else:
                    tokens = self.board.get_tokens_by_pixel(data)
                    if tokens:
                        tokens[0].turn_left(5)


class TokenButton(ToolbarWidget):

    def __init__(self, token_type, board, parent):
        super().__init__()
        self.parent = parent
        self.board = board
        # token = token_type(position = None)
        print(token_type, token_type.class_image)
        if token_type.class_image:
            self._img_path = token_type.class_image
        self._text_padding = 30
        self.set_text("Add " + token_type.__name__)
        self.token_type = token_type
        self.background_color = (180, 180, 180, 255)

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
