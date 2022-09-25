import miniworldmaker.tokens.token_plugins.text_token.text_costume as text_costume
import miniworldmaker.tokens.token as token


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

    def __init__(self, position=None, text=" "):
        super().__init__(position)
        self.costume = text_costume.TextCostume(self)
        self.costume.font_size = 24
        self.costume.is_scaled = True
        self.costume.text = ""
        self.is_static: bool = True
        self.set_text(text)
        self.fixed_size = False

    def _get_new_costume(self):
        return text_costume.TextCostume(self)

    @property
    def font_size(self):
        return self.costume.font_size

    @font_size.setter
    def font_size(self, value):
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

    def get_text(self):
        """Gets the currently displayed tex

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


class TextToken(Text):
    """Alias for legacy code"""

    pass
