from typing import Tuple, Union

from miniworldmaker.tokens import token
from miniworldmaker.exceptions.miniworldmaker_exception import CantSetAutoFontSize, MiniworldMakerError


class Text(token.Token):
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

        Create a new text_token::

            self.text = TextToken((1,1), "Hello World")


    """

    def __init__(self, position=None, t=" "):
        super().__init__(position)
        self.add_costume((0, 0, 0, 0))
        self.costume.fill_color = (0, 0, 0, 0)
        self.costume.font_size = 24
        self.costume.is_scaled = True
        self.costume.text = ""
        self.is_static: bool = True
        self.set_text(t)

    @property
    def font_size(self):
        return self.costume.font_size

    @font_size.setter
    def font_size(self, value):
        self.costume.font_size = value
        self._update_text()

    def set_text(self, text):
        """
        Sets the text of the token

        Args:
            text: The text
        """
        self.costume.text = text
        self._update_text()

    def get_text(self):
        """Gets the currently displayed tex

        Returns:
            The currently displayed text

        """
        return self.costume.text

    @property
    def text(self):
        """changes the text."""
        self.get_text()

    @text.setter
    def text(self, value):
        if value == "":
            value = " "
        self.set_text(value)
        self._update_text()

    def _update_text(self):
        """Sets self.size by costume.font_size"""
        if not self.board.fixed_size:
            self.set_size((self.costume.get_text_width(), self.costume.font_size), auto_size=False)
        if self.board.fixed_size:
            self.costume.font_size = 0
            while self.costume.get_text_width() < self.size[0] and self.costume.font_size < self.size[1]:
                self.costume.font_size += 1

    def set_size(self, value, auto_size=True):
        super().set_size(value)


class TextToken(Text):
    """Alias for legacy code"""

    pass
