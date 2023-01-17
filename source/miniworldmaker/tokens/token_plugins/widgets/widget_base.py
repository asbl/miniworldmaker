from typing import Union

import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tokens.token_plugins.widgets.widget_costume as widget_costume

class BaseWidget(token_mod.Token):
    def __init__(self):
        super().__init__()
        self._position = (0, 0)
        # Paddings and margins
        self._padding_top = 5
        self._padding_left = 5
        self._padding_right = 5
        self._padding_bottom = 5
        self.margin_top = 5
        self.margin_left = 5
        self.margin_right = 5
        self.margin_bottom = 5
        self._text_align = "left"
        self._row_height = 20
        # additional layout
        self.fixed_width: bool = True
        self._overflow = False
        # additional
        self.timed = False  # e.g. for counters
        super().__init__((0, 0))

    def new_costume(self):
        return widget_costume.WidgetCostume(self)

    @property
    def value(self):
        return self.token_id

    def resize(self):
        pass

    def update_positions(self):
        pass

    @property
    def padding_left(self):
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value):
        self._padding_left = value
        self.resize()

    text_padding_left = padding_left

    @property
    def padding_right(self):
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value):
        self._padding_right = value
        self.resize()

    text_padding_right = padding_right

    @property
    def padding_top(self):
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value):
        self._padding_top = value
        self.resize()

    text_padding_top = padding_top

    @property
    def padding_bottom(self):
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        self._padding_bottom = value
        self.resize()

    text_padding_bottom = padding_bottom

    @property
    def position(self):
        return self.position_manager.get_position()

    @position.setter
    def position(self, value):
        self.position_manager.set_position(value)
        self.update_positions()

    @property
    def topleft(self):
        return self.position_manager.get_position()

    @topleft.setter
    def topleft(self, value):
        self.position_manager.set_position(value)
        self.update_positions()

    @property
    def center(self):
        return self.position_manager.get_center()

    @center.setter
    def center(self, value):
        self.position_manager.set_center(value)
        self.update_positions()

    @property
    def row_height(self):
        return self._row_height

    @row_height.setter
    def row_height(self, value):
        self.set_row_height(value)

    def set_row_height(self, value):
        self._row_height = value

    def set_border(self, color: tuple = (0, 0, 0, 255), width: int = 1):
        """sets border of widget

        Args:
            color (_type_): _description_
            width (_type_): _description_
        """
        self.border_color = color
        self.border = width

    def set_board(self, new_board):
        super().set_board(new_board)
        # for child in self.children:
        #    if isinstance(child, self.BaseWidget):
        #        child.resize()
        # child.costume._update_draw_shape()

    def set_position(self, value: Union["board_position.Position", tuple]):
        super().set_position(value)
        self.resize()
        self.costume._update_draw_shape()
