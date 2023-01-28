import logging
from typing import Union

import miniworldmaker.tokens.token_plugins.shapes.shapes as shapes
import miniworldmaker.tokens.token_plugins.widgets.buttonwidget as widget
from miniworldmaker.exceptions.miniworldmaker_exception import NoValidBoardPositionError


class Input(widget.ButtonWidget):
    def __init__(self, position):
        super().__init__("")
        self.background_color = (255, 255, 255, 0)
        try:
            self.position = position
        except NoValidBoardPositionError:
            raise NoValidBoardPositionError(position)
        self._max_chars = 10
        self.fixed_width = 20  # (self._max_chars * self.text.font_size) / 2
        self.current_input = ""
        self._cursor_position = 0
        self.cursor_x = self.x
        self.cursor = shapes.Line((0, 0), (100, 100))  # set in update_cursor
        self.cursor.border_color = (255, 255, 255, 255)
        self.fixed_width = True
        self.is_focusable = True
        cursor = self.cursor  # for decorator

        @cursor.register
        def act(self):
            if self._parent.has_focus:
                if self.board.frame % 20 == 0 and not self.board.frame % 40 == 0:
                    self.hide()
                if self.board.frame % 40 == 0:
                    self.show()
            else:
                self.hide()

        self.update_cursor()
        self.add_child(self.cursor)

    def has_focus(self):
        if self.board.event_manager.focus_token == self:
            return True
        else:
            return False

    @property
    def max_chars(self):
        return self._max_chars

    @max_chars.setter
    def max_chars(self, value):
        self._max_chars = value
        self.resize()

    def resize(self):
        """ resizes widget based on text_width and height
        """
        super().resize()  # sets fixed width
        if self.board.is_tiled:
            return
        if self._img:
            # self._img.width = self.row_height
            self._img.height = self.row_height - self.padding_top - self.padding_bottom
            self._img.width = self._img_width
            self._img.position = self.position[0] + self.padding_left, self.position[1] + self.padding_top
        if not self.fixed_width:
            # no image: Set width/height by text and img width
            if self._text_align == "left" and not self._img:
                self.width = self.text.width
            elif self._text_align == "left" and self._img or self._text_align == "image":
                self.width = self.text.width + self._padding_left + self._padding_right + self._img_width + self.img_padding_right
        self.height = self.text.height + self._padding_top + self._padding_bottom
        self.update_positions()
        self.cut_text()

    def update_cursor(self):
        font_size = self.text.font_size
        if self.cursor_position == 0:
            self.cursor_x = self.x
        else:
            self.cursor_x = self.x + self.text.costume.font_manager.get_text_width(
                self.current_input[0:self.cursor_position])
        self.cursor.start_position = (self.cursor_x + font_size / 2, self.y)
        self.cursor.end_position = (self.cursor_x + font_size / 2, self.y + self.height)

    @property
    def cursor_position(self):
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, value):
        self._cursor_position = value
        self.update_cursor()

    def set_text(self, text: Union[str, int, float]):
        self.current_input = text
        super().set_text(text)

    def on_key_down(self, keys):
        if self.has_focus:
            if "SHIFT_L" in keys:
                pass
            elif "LEFT" in keys and self.cursor_position > 0:
                self.cursor_position -= 1
            elif "RIGHT" in keys and self.cursor_position < len(self.current_input):
                self.cursor_position += 1
            elif "BACKSPACE" in keys:
                if 0 < self.cursor_position <= len(self.current_input):
                    self.cursor_position -= 1
                    self.set_text(
                        self.current_input[0:self.cursor_position] + self.current_input[self.cursor_position + 1:])
            else:
                text = keys[-1]
                if text != "":
                    self.set_text(
                        self.current_input[0:self.cursor_position] + text + self.current_input[self.cursor_position:])
                    self.cursor_position += 1
                    self.update_cursor()
                    logging.info("CURSOR", self.cursor.x, self.cursor.y, self.cursor.width, self.cursor.height)

    def on_focus(self):
        print("focus")

    def on_focus_lost(self):
        print("focus lost")