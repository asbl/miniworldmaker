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

    """
    def __init__(self, position = None, text = "", font_size = 80, color = (255, 255, 255, 255)):
        super().__init__(position)
        self.costume.fill_color=(0, 0, 0, 0)
        self.costume.font_size = font_size
        self.costume.text = text
        self.costume.color = color
        self.costume.is_scaled = True

    def set_text(self, text):
        """
        Sets the text of the token

        Args:
            text: The text
        """
        self.costume.text = text
        self.costume.call_action(("text"))

    def get_text(self):
        """
        Gets the currently displayed tex

        Returns: The currently displayed text

        """
        self.costume.call_action("text changed")
        return self.costume.text