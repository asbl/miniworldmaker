from miniworldmaker.tokens import token


class TextToken(token.Token):
    """
    A Text-Token is a token which contains a Text.

    You have to set the size of the token with self.size() manually so that
    the complete text can be seen.

    Args:
        position: Top-Left position of Text
        text: The initial text
        font-size: The size of the font (default: 80)
        color: The color of the font (default: white)

    Examples:
        >>> self.text = TextToken((1,1), "Hello World")
        Creates a new text_token

    """

    def __init__(self, position=None, text="", font_size=80, color=(255, 255, 255, 255)):
        super().__init__(position, None)
        self.add_costume((0,0,0,0))
        self.costume.fill_color = (0, 0, 0, 0)
        self.costume.font_size = font_size
        self.costume.color = color
        self.costume.is_scaled = True
        self.costume.text = text
        self._auto_size = False
        self._auto_font_size = True
        self.is_static = True
        self.set_text(text)

    def set_text(self, text):
        """
        Sets the text of the token

        Args:
            text: The text
        """
        self.costume.text = text
        self.set_auto_size()

    def get_text(self):
        """
        Gets the currently displayed tex

        Returns: The currently displayed text

        """
        return self.costume.text

    def set_auto_size(self):
        if self.auto_size:
            self.size = (self.costume.font_size * len(self.costume.text), self.costume.font_size)
        elif self.auto_font_size:
            if len(self.costume.text) != 0:
                self.costume.font_size = int(min(self.size[0] / len(self.get_text()), self.size[1]))
            else:
                self.costume.font_size = int(min(self.size[0], self.size[1]))

    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value
        if self._auto_size is True:
            self._auto_font_size = False

    @property
    def auto_font_size(self):
        return self._auto_font_size

    @auto_font_size.setter
    def auto_font_size(self, value):
        self._auto_font_size = value
        if self._auto_font_size is True:
            self._auto_size = False

    def set_size(self, value):
        super().set_size(value)
        self.set_auto_size()
