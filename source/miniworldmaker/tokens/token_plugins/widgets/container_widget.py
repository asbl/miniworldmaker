from typing import Union

import miniworldmaker.tokens.token_plugins.container_token as container_token
import miniworldmaker.tokens.token_plugins.widgets.widget_base as widget_base


class ContainerWidget(container_token.ContainerToken, widget_base.BaseWidget):
    """Widget containing multiple widgets.

    The widgets inside of this widget are displayed from left to right.
    """

    def __init__(self, children):
        self._inner_padding = 5
        self._padding_top = 2
        self._padding_left = 0
        self._padding_right = 0
        self._padding_bottom = 0
        widget_base.BaseWidget.__init__(self)
        container_token.ContainerToken.__init__(self)
        self.set_background_color((255, 255, 255, 0))
        for child in children:
            self.add_child(child)
            child.resize()

    def set_board(self, new_board):
        super().set_board(new_board)
        for child in self.children:
            child.set_board(new_board)

    @property
    def inner_padding(self):
        if hasattr(self, "_inner_padding"):
            return self._inner_padding
        else:
            return 0

    def resize(self):
        super().resize()
        actual_x = self.x + self.padding_left  # saves current c position, will be changed in loop
        for child in self.children:
            # set child positions
            child.row_height = child.height
            child.width = (self.width - self.inner_padding - self.padding_right - self.padding_left) / len(
                self.children)
            child.height = self.height - self.padding_top - self.padding_bottom
            child.x = actual_x
            child.y = self.y + self.padding_top
            child.update_positions()
            actual_x += child.width + self.inner_padding

    def get_widget(self, pos):
        local_pos = self.get_local_pos(pos)
        actual_x = 0
        for child in self.children:
            if actual_x <= local_pos[0] <= actual_x + child.width:
                return child
            actual_x += child._width + self.inner_padding

    def add_child(self, token: "token_mod.Token"):
        super().add_child(token)
        token.row_height = self.row_height

    def set_row_height(self, value):
        self._row_height = value
        for child in self.children:
            child.row_height = value

