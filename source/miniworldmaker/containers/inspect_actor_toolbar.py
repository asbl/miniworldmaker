import miniworldmaker.positions.position as board_position
import miniworldmaker.containers.toolbar as toolbar
from miniworldmaker.containers.widgets import ToolbarLabel
from miniworldmaker.containers.widgets import ToolbarButton


class InspectActorToolbar(toolbar.Toolbar):

    def __init__(self, board):
        super().__init__()
        self.position = "right"
        self.board = board
        self.actor = None
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.default_size = 280
        self.active_token = None
        self.direction_label = 0
        self.position_label = 0

    def set_active_token(self, token):
        self.active_token = token
        self.active_token.costume.info_overlay = True
        token.dirty = 1
        self.board.app.event_manager.to_event_queue("active_token", token)
        return token

    def get_active_token_from_board_position(self, pos):
        # Test an token was clicked and set the active token
        tokens = self.board.get_tokens_from_pixel(pos)
        if tokens:
            i = 0
            # Find the token under the currently selected token.
            while i < len(tokens):
                if self.active_token == tokens[i]:
                    if i < len(tokens) - 1:
                        return tokens[i + 1]
                    else:
                        return tokens[0]
                i = i + 1
        if not tokens:
            return None
        if not self.active_token in tokens:
            return tokens[0]

    def add_to_window(self, window, dock, size=None):
        super().add_to_window(window, dock, size)
        for actor in self.board.tokens:
            # if self.actor.__class__ == act.Actor:
            self.add_widget(TokenButton(token=actor, toolbar=self))

    def _set_active_token_from_mouse(self, event, data):
        if event and "mouse" in event and self.board.get_mouse_position():
            mouse_pos = board_position.Position.create(self.board.get_mouse_position())
            if self.board.contains_position(mouse_pos) and event == "mouse_left":
                token = self.get_active_token_from_board_position(data)
                if token:
                    self.set_active_token(token)

    def _replace_active_token(self, event, data):
        self.actor = data
        self.remove_all_widgets()
        self.add_widget(ToolbarLabel("Class: " + str(self.actor.__class__.__name__)))
        self.add_widget(ToolbarLabel("ID: " + str(self.actor.token_id)))
        self.direction_label = self.add_widget(
            ToolbarLabel("Direction: " + str(self.actor.direction)))
        rounded_position = "Position: (" + str(round(self.actor.position[0], 0)) + "," + str(
            round(self.actor.position[1], 0)) + ")"
        self.position_label = self.add_widget(ToolbarLabel(rounded_position))

    def _update_active_token_data(self, event, data):
        if self.direction_label and self.position_label:
            self.direction_label = self.direction_label.set_text(
                "Direction: " + str(self.actor.direction))
            rounded_position = "Position: (" + str(round(self.actor.position[0], 0)) + "," + str(
                round(self.actor.position[1], 0)) + ")"
            self.position_label = self.position_label.set_text(rounded_position)

    def handle_event(self, event, data):
        self._set_active_token_from_mouse(event, data)
        super().get_event(event, data)
        if event == "active_token":
            self.actor = data
        if self.actor is not None:
            if event == "active_token" or "token" in event:
                self._replace_active_token(event, data)
            else:
                self._update_active_token_data(event, data)
        else:
            for an_actor in self.board.tokens:
                if self.actor:
                    self.add_widget(TokenButton(token=an_actor))


class TokenButton(ToolbarButton):

    def __init__(self, token, toolbar):
        super().__init__(text=str(token.__class__.__name__) + " at " + str(token.position))
        self.token = token
        self._img_path = token.costume.image_manager.get_source_from_current_image()
        self.toolbar = toolbar
        self._text_padding = 30

    def get_event(self, event, data):
        if not self.toolbar.active_token == self.token:
            self.toolbar.set_active_token(token=self.token)

    def __str__(self):
        return "ActorButton, {0} at pos: {1}".format(self.token, self.token.position)
