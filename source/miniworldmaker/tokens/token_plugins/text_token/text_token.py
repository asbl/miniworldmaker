import miniworldmaker.tokens.token as token
import miniworldmaker.tokens.token_plugins.text_token.text_costume as text_costume


class Text(token.Token):
    """
    A Text-Token is a token which contains a Text.

    You have to set the sget_tokens_atize of the token with self.size() manually so that
    the complete text can be seen.

    Args:
        position: Top-Left position of Text.
        text: The initial text

    Examples:

        Create a new text_token::

            self.text = TextToken((1,1), "Hello World")
    """

    def __init__(self, position=None, text: str = " "):
        self._max_width = 0
        super().__init__(position)
        self.font_size = 24
        self.costume.is_scaled = True
        self.is_static: bool = True
        self.fixed_size = False
        self.set_text(text)

    def new_costume(self):
        return text_costume.TextCostume(self)

    @property
    def font_size(self):
        return self.costume.font_size

    @font_size.setter
    def font_size(self, value):
        if self.costume:
            self.costume.font_size = value
            self.costume._update_draw_shape()
            self.costume.set_dirty("write_text", self.costume.RELOAD_ACTUAL_IMAGE)

    def set_text(self, text):
        """
        Sets the text of the token

        Args:
            text: The text
        """
        self.costume.text = text
        self.costume._update_draw_shape()
        self.costume.set_dirty("write_text", self.costume.RELOAD_ACTUAL_IMAGE)

    def font_by_size(self, width=None, height=None):
        self.font_size = self.costume.scale_to_size(width, height)

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        self._max_width = value
        self.costume._update_draw_shape()
        self.costume.set_dirty("write_text", self.costume.RELOAD_ACTUAL_IMAGE)

    def get_text_width(self):
        return self.costume.get_text_width()

    def get_text_width(self):
        return self.costume.get_text_width()

    def get_text(self):
        """Gets the currently displayed text

        Returns:
            The currently displayed text

        """
        return self.costume.text

    @property
    def text(self):
        """changes the text."""
        return self.get_text()

    @text.setter
    def text(self, value):
        if value == "":
            value = " "
        self.set_text(value)
        self.costume.set_dirty("all", self.costume.RELOAD_ACTUAL_IMAGE)

    def on_shape_change(self):
        self.costume._update_draw_shape()


class TextToken(Text):
    """Alias for legacy code"""

    pass
