
from typing import Tuple, Union

from miniworldmaker.tokens import token
from miniworldmaker.exceptions.miniworldmaker_exception import CantSetAutoFontSize, MiniworldMakerError


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
        
        Create a new text_token::
        
            self.text = TextToken((1,1), "Hello World")
        

    """

    def __init__(self, position=None, text: str = "", font_size: int = 80, color: Tuple[int, int, int, int] = (255, 255, 255, 255)):
        super().__init__(position, None)
        self.add_costume((0, 0, 0, 0))
        self.costume.fill_color = (0, 0, 0, 0)
        self.costume.font_size = font_size
        self.costume.color = color
        self.costume.is_scaled = True
        self.costume.text = text
        self._auto_size: str = "font"
        self.is_static: bool = True
        self.set_text(text)
        
    @property 
    def auto_size(self):
        """Gets auto size value:
          * "token": token is autosized by font size
          * "font": font is autosized by token size
          * None: no autosizing
        """
        return self._auto_size
    
    @auto_size.setter
    def auto_size(self, value: Union[None, str]):
        self._auto_size = value
        self.set_auto_size()
        
    @property        
    def font_size(self):
        return self.costume.font_size
    
    @font_size.setter
    def font_size(self, value):
        if self.auto_size == "font":
            raise CantSetAutoFontSize()
        self.costume.font_size = value
        self.set_auto_size()
            
    def set_text(self, text):
        """
        Sets the text of the token

        Args:
            text: The text
        """
        self.costume.text = text
        self.set_auto_size()

    def get_text(self):
        """Gets the currently displayed tex

        Returns: 
            The currently displayed text

        """
        return self.costume.text

    def set_auto_size(self):
        """Sets self.size by costume.font_size
        """
        if self.auto_size == "token":
            self.set_size((self.costume.font_size * len(self.costume.text), self.costume.font_size), auto_size = False)
        elif self.auto_size == "font":
            if len(self.costume.text) != 0:
                self.costume.font_size = int(
                    min(self.size[0] / len(self.get_text()), self.size[1]))
            else:
                self.costume.font_size = int(min(self.size[0], self.size[1]))

    def set_size(self, value, auto_size = True):
        super().set_size(value)
        if auto_size:
            self.set_auto_size()
