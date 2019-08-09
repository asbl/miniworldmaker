from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *


class ColorToolbar(toolbar.Toolbar):
    """
    A toolbar to get the background color at a specific pixel
    """

    def __init__(self, board):
        super().__init__()
        self.registered_events.add("all")
        self.registered_events.add("debug")
        self.board = board
        self.default_size = 220
        self.color_label = ColorLabel("Color")
        self.add_widget(self.color_label)

    def get_event(self, event, data):
        if "mouse_left" in event:
            if self.board.is_in_container(data[0], data[1]):
                self.color_label.set_text(str(self.board.background.color_at(data)))
                self.color_label.set_color(self.board.background.color_at(data))


class ColorLabel(ToolbarLabel):
    def __init__(self, text):
        super().__init__(text)

    def set_color(self, color):
        self.background_color = color
        self.dirty = 1