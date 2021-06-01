from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *


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
        self.window.send_event_to_containers("active_token", token)
        return token

    def get_active_token_from_board_position(self, pos):
        # Test an token was clicked and set the active token
        tokens = self.board.get_tokens_by_pixel(pos)
        if tokens:
            i = 0
            # Find the token under the currently selected token.
            while i < len(tokens):
                if self.active_token == tokens[i]:
                    if i < len(tokens) - 1:
                        return tokens[i + 1]
                        break
                    else:
                        return tokens[0]
                        break
                i = i + 1
        if not tokens:
            return None
        if not self.active_token in tokens:
            return tokens[0]

    def _add_to_window(self, window, dock, size=None):
        super()._add_to_window(window, dock, size)
        for actor in self.window.board.tokens:
            # if self.actor.__class__ == act.Actor:
            self.add_widget(TokenButton(token=actor, toolbar=self))

    def handle_event(self, event, data):
        if event and "mouse" in event and self.board.get_mouse_position() and self.board.get_mouse_position().is_on_board():
            if event == "mouse_left":
                token = self.get_active_token_from_board_position(data)
                if token:
                    self.set_active_token(token)
        super().get_event(event, data)
        if event == "active_token":
            self.actor = data
        if self.actor is not None:
            if event == "active_token" or "token" in event:
                self.actor = data
                self.remove_all_widgets()
                self.add_widget(ToolbarLabel("Class: " + str(self.actor.__class__.__name__)))
                self.add_widget(ToolbarLabel("ID: " + str(self.actor.token_id)))
                self.direction_label = self.add_widget(ToolbarLabel("Direction: " + str(self.actor.direction)))
                rounded_position = "Position: (" + str(round(self.actor.position[0], 0)) + "," + str(
                    round(self.actor.position[1], 0)) + ")"
                self.position_label = self.add_widget(ToolbarLabel(rounded_position))
                method_list = [func for func in self.actor.__class__.__dict__ if
                               not func.startswith("_") and not func in ['get_event', 'class_image']]
                for method in method_list:
                    self.add_widget(
                        MethodButton(text="--> call method: {0}".format(method), actor=self.actor, method=method))
            else:
                if self.direction_label and self.position_label:
                    self.direction_label = self.direction_label.set_text("Direction: " + str(self.actor.direction))
                    rounded_position = "Position: (" + str(round(self.actor.position[0], 0)) + "," + str(round(self.actor.position[1],0)) + ")"
                    self.position_label = self.position_label.set_text(rounded_position)


        else:
            for an_actor in self.window.board.tokens:
                if self.actor:
                    self.add_widget(TokenButton(token=an_actor))


class MethodButton(ToolbarButton):

    def __init__(self, text, actor, method):
        super().__init__(text=text)
        self.actor = actor
        self.method = method

    def get_event(self, event, data):
        if self.actor is not None:
            getattr(self.actor, str(self.method))()

    def __str__(self):
        return "MethodButton, {0}".format(self.actor)


class TokenButton(ToolbarButton):

    def __init__(self, token, toolbar):
        super().__init__(text=str(token.__class__.__name__) + " at " + str(token.position))
        self.token = token
        if token.costume.image_paths:
            self._img_path = token.costume.image_paths[0]
        self.toolbar = toolbar
        self._text_padding = 30

    def get_event(self, event, data):
        if not self.toolbar.active_token == self.token:
            self.toolbar.set_active_token(token=self.token)

    def __str__(self):
        return "ActorButton, {0} at pos: {1}".format(self.token, self.token.position)
