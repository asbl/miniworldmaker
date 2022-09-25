import os

import miniworldmaker.tokens.token as token
from miniworldmaker.positions import rect as board_rect
from miniworldmaker.positions import position as board_position
from miniworldmaker.containers import toolbar
from miniworldmaker.containers import widgets
from miniworldmaker.exceptions import miniworldmaker_exception


class LevelDesignerToolbar(toolbar.Toolbar):

    def __init__(self, board, token_classes, file):
        super().__init__()
        self.board = board
        self.default_size = 400
        self.app = board.app
        self.selected_token_type = None
        self.dummy = None
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.add_widget(widgets.ToolbarLabel("Left Click to add Tokens"))
        self.add_widget(widgets.ToolbarLabel("Right Click or Wheel to change direction"))
        self.add_widget(widgets.ToolbarLabel("SHIFT + Right Click to delete token"))
        self.prototypes = dict()
        for cls in token_classes:
            prototype = cls((-100, -100))
            prototype.export = False
            self.prototypes[cls.__name__] = prototype
            button = TokenButton(token_type=cls, board=board, parent=self, prototype=prototype)
            self.add_widget(button, cls.__name__)
        db_file = file
        self.add_widget(widgets.SaveButton(board=self.board, text="Save", filename=db_file))
        if os.path.exists(db_file):
            self.add_widget(widgets.LoadButton(board=self.board, text="Load", filename=db_file))
        self.add_widget(widgets.ClearButton(board=self.board, text="Clear"))

    def _add_token_to_mouse_position(self, mouse_pixel_pos):
        position = board_position.Position.from_pixel(mouse_pixel_pos)
        if self.selected_token_type:
            prototype = self.prototypes[self.selected_token_type.__name__]
            rect = board_rect.Rect.from_token(prototype)
            rect.topleft = mouse_pixel_pos
            tokens = [token for token in self.board.tokens if token.detect_rect(rect)]
            # remove dummy
            if self.dummy and tokens and self.dummy in tokens:
                tokens.remove(self.dummy)
            # add tokens if no tokens are at current position
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
        # preprocess - Get Position and token at position (max: 1)
        pixel_position = data
        position = board_position.Position.from_pixel(data)
        keys = self.board.app.event_manager.get_keys()
        tokens = self.board.get_tokens_at_position(position)
        # remove dummy from tokens
        if self.dummy in tokens:
            tokens.remove(self.dummy)
        # select token at position, if there is a token
        if not tokens:
            token = None
        elif len(tokens) == 1:
            token = tokens[0]
        else:
            raise Exception(f"tokens is {tokens}, should be None or should have len 1")
        # Event handling
        if "mouse_left" in event:
            if not tokens and not keys:
                self._add_token_to_mouse_position(pixel_position)
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

    def _update_dummy(self, position):
        if self.dummy:
            self.dummy.position = position
            tokens = self.dummy.detect_tokens()
            if self.dummy and tokens and self.dummy in tokens:
                tokens.remove(self.dummy)
            if tokens:
                self.dummy.switch_costume(1)
            else:
                self.dummy.switch_costume(0)

    def get_event(self, event, data):
        super().get_event(event, data)
        if type(data) == tuple and self.bboard.is_in_container(data[0], data[1]):
            self.handle_board_event(event, data)


class Dummy(token.Token):
    def on_setup(self):
        self.add_costume((0, 0, 0, 100))
        self.add_costume((255, 0, 0, 100))
        self.export = False


class TokenButton(widgets.Widget):

    def __init__(self, token_type, board, parent, prototype):
        super().__init__("Button")
        self.parent = parent
        self.board = board
        self._img_path = prototype.costume.image_manager.get_source_from_current_image()
        self._text_padding = 30
        self.set_text("Add " + token_type.__name__)
        self.token_type = token_type
        self.background_color = (180, 180, 180, 255)

    def get_event(self, event, data):
        if event == "mouse_left":
            self.board.app.event_manager.to_event_queue(
                "Selected actor", self.token_type)
            self.parent.selected_token_type = self.token_type
            prototype = self.parent.prototypes[self.parent.selected_token_type.__name__]
            if self.parent.dummy:
                self.parent.dummy.remove()
            self.parent.dummy = Dummy((0, 0))
            if not self.board.tokens_fixed_size:
                self.parent.dummy.size = prototype.size
            for widget in self.parent.widgets:
                if widget.__class__ == TokenButton:
                    widget.background_color = (180, 180, 180, 255)
                    widget.dirty = 1
            self.background_color = (100, 100, 100, 255)
            self.dirty = 1
