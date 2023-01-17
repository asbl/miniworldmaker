from typing import Union

import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tokens.token_plugins.container_token as container_token
import miniworldmaker.tokens.token_plugins.text_token.text_token as text_token
import miniworldmaker.tokens.token_plugins.widgets.widget_base as widget_base
import miniworldmaker.tokens.token_plugins.widgets.widget_parts as widget_parts

class ButtonWidget(container_token.ContainerToken, widget_base.BaseWidget):
    def __init__(self, text="", image=""):
        # constructors
        widget_base.BaseWidget.__init__(self)
        container_token.ContainerToken.__init__(self)
        # container_widget.ContainerWidget.__init__(self)

        # text
        self._img = None
        self._text = widget_parts.WidgetText((0, 0), text)
        self._text.font_size = 15
        self._text_align = "left"
        # additional layout
        self.overflow = False
        # additional
        self.children = []
        # image
        self._img_width = 22
        self._img_source = None
        self.img_padding_right = 5
        if image:
            self.set_image(image)
        # text attributes
        self.set_text(text)
        # additional layout 2
        self.set_background_color((60, 60, 60))
        self.add_child(self._text)

    def set_image(self, _img_source: Union[str, tuple]):
        """sets image of widget

        Args:
            _img_source (str): path to image or tuple with color
        """
        if self._img and self._img in self.children:
            self.remove_child(self._img)
        self._img = widget_parts.WidgetImage()
        self._img.add_costume(_img_source)
        self._img.width = self._img_width
        self._img.height = self.text.height
        self.add_child(self._img)
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

    def cut_text(self):
        if self.fixed_width:
            if not self.overflow:
                if not self._img:
                    self.text.max_width = self.width - self.padding_left - self.padding_right
                if self._img:
                    self.text.max_width = self.width - self.padding_left - self.padding_right - self._img_width - self.img_padding_right

    def on_shape_change(self):
        self.cut_text()

    def update_positions(self):
        super().update_positions()
        """updates text and img position"""
        if self._text_align == "left" and not self._img:
            self.text.position = self.position[0] + self.padding_left, self.position[1] + self.padding_top
        if self._text_align == "left" and self._img or self._text_align == "image":
            self._img.position = self.position[0] + self.padding_left, self.position[1] + self.padding_top
            self.text.position = self.position[0] + self._img_width + self.img_padding_right + self.padding_left, \
                                 self.position[1] + self.padding_top
        self.text.costume._update_draw_shape()

    def set_row_height(self, value=20):
        super().set_row_height(value)
        self.text.font_by_size(self.width, value - self.padding_top - self.padding_bottom)
        self.resize()

    def get_local_pos(self, position):
        x = position[0] - self.topleft[0]
        y = position[1] - self.topleft[1]
        return x, y

    @property
    def text_align(self):
        """Defines how text is aligned.

        If widget has an image, text is aligned left, else it can be set to "left", "center" or "right".
        """
        if not self._img_source:
            return "left"
        else:
            return self._text_align

    @text_align.setter
    def text_align(self, value):
        self._text_align = value
        self.dirty = 1
        self.resize()

    @property
    def value(self):
        return self.text.text

    @property
    def text(self) -> text_token.Text:
        """The text which is displayed on the widget."""
        return self._text

    @text.setter
    def text(self, value: str):
        self.set_text(value)

    def set_text(self, text: Union[str, int, float]):
        """Sets text of widget.

        int and float values are converted to string.
        """
        if type(text) == int or type(text) == float:
            text = str(text)
        self.text.set_text(text)
        self.max_width = self.text.width
        self.max_height = self.text.height
        self.resize()

    def remove(self, kill=True):
        self.text.remove()
        super().remove()
