import os

from miniworldmaker.board_positions import board_position, board_rect_factory, board_position_factory
from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import SaveButton, LoadButton, ToolbarWidget, ToolbarLabel, ToolbarButton
from miniworldmaker.tokens import token
from miniworldmaker.containers.toolbar_widgets import ClearButton
from miniworldmaker.exceptions import miniworldmaker_exception

class LevelDesignerToolbar(toolbar.Toolbar):

    def __init__(self, board, token_classes, file):
        super().__init__()
        self.default_size = 400
        self.app = board.app
        self.selected_token_type = None
        self.dummy = None
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.add_widget(ToolbarLabel("Left Click to add Tokens"))
        self.add_widget(ToolbarLabel("Right Click or Wheel to change direction"))
        self.add_widget(ToolbarLabel("SHIFT + Right Click to delete token"))
        self.prototypes = dict()
        for cls in token_classes:
            prototype = cls((-100,-100))
            prototype.export = False
            self.prototypes[cls.__name__] = prototype
            self.add_widget(TokenButton(cls, board, self, self.prototypes[cls.__name__]))
        db_file = file
        self.add_widget(SaveButton(board=self.app.board, text="Save", filename=db_file))
        if os.path.exists(db_file):
            self.add_widget(LoadButton(board=self.app.board, text="Load", filename=db_file))
        self.add_widget(ClearButton(board=self.app.board, text="Clear"))

    def _add_token_to_mouse_position(self, position,):
        if self.selected_token_type:
            prototype = self.prototypes[self.selected_token_type.__name__]
            size = prototype.size
            rect = board_rect_factory.BoardRectFactory(self.app.board).from_position(position, size)
            tokens = self.app.board.get_tokens_at_rect(rect)
            if self.dummy and tokens and self.dummy in tokens:
                tokens.remove(self.dummy)
            if tokens:
                print("Can't create overlapping tokens")
            else:
                self.selected_token_type(position)

    def _remove_token_from_mouse_position(self, token):
        token.remove()

    def _change_direction_at_mouse_position(self, token, direction):
        if direction == "left":
            token.turn_left(5)
        elif direction == "right":
            token.turn_right(5)

    def _select_token(self, token):
        pass

    def handle_board_event(self, event, data):
        # preprocess - Get BoardPosition and token at position (max: 1)
        position = board_position_factory.BoardPositionFactory(self.app.board).from_pixel(data)
        keys = self.app.board.app.event_manager.get_keys()
        tokens = self.app.board.get_tokens_by_pixel(position)
        if self.dummy in tokens:
            tokens.remove(self.dummy)
        if not tokens:
            token = None
        elif len(tokens) == 1:
            token = tokens[0]
        else:
            raise Exception()
        # Event handling
        if "mouse_left" in event:
            if not tokens and not keys:
                self._add_token_to_mouse_position(position)
            else:
                self._select_token(token)
        elif "wheel_up" in event:
            self._change_direction_at_mouse_position(token, "left")
        elif "wheel_down" in event:
            self._change_direction_at_mouse_position(token, "right")
        elif "mouse_right" in event:
            if keys and "L_SHIFT" in keys:
                self._remove_token_from_mouse_position(token)
            else:
                self._change_direction_at_mouse_position(token, "left")
        self._update_dummy(position)


    def _update_dummy(self, data):
        position = board_position_factory.BoardPositionFactory(self.app.board).create(data)
        if self.dummy:
            self.dummy.position = position
            rect = board_rect_factory.BoardRectFactory(self.app.board).from_position(self.dummy.position, self.dummy.size)
            tokens = self.app.board.get_tokens_at_rect(rect)
            if self.dummy and tokens and self.dummy in tokens:
                tokens.remove(self.dummy)
            if tokens:
                self.dummy.switch_costume(1)
            else:
                self.dummy.switch_costume(0)

    def get_event(self, event, data):
        super().get_event(event, data)
        if type(data) == tuple and self.app.board.is_in_container(data[0], data[1]):
            self.handle_board_event(event, data)

class Dummy(token.Token):
    def on_setup(self):
        self.add_costume((0,0,0,100))
        self.add_costume((255,0,0,100))
        self.export = False


class TokenButton(ToolbarWidget):

    def __init__(self, token_type, board, parent, prototype):
        super().__init__()
        self.parent = parent
        self.board = board
        if prototype.costume.image_paths:
            self._img_path = prototype.costume.image_paths[0]
        self._text_padding = 30
        self.set_text("Add " + token_type.__name__)
        self.token_type = token_type
        self.background_color = (180, 180, 180, 255)

    def get_event(self, event, data):
        if event == "mouse_left":
            self.board.app.event_manager.send_event_to_containers(
                "Selected actor", self.token_type)
            self.parent.selected_token_type = self.token_type
            prototype = self.parent.prototypes[self.parent.selected_token_type.__name__]
            if self.parent.dummy:
                self.parent.dummy.remove()
            self.parent.dummy = Dummy((0,0))
            try:
                self.parent.dummy.size = prototype.size
            except miniworldmaker_exception.SizeOnTiledBoardError:
                print("Set autosize on tiled board")
            for widget in self.parent.widgets:
                if widget.__class__ == TokenButton:
                    widget.background_color = (180, 180, 180, 255)
                    widget.dirty = 1
            self.background_color = (100, 100, 100, 255)
            self.dirty = 1
