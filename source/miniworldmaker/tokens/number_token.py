from miniworldmaker.tokens import text_token


class NumberToken(text_token.TextToken):
    """
    A number token shows a Number.

    You have to set the size of the token with self.size() manually so that
    the complete text can be seen.

    Args:
        position: Top-Left position of Number
        number: The initial number
        font-size: The size of the font (default: 80)
        color: The color of the font (default: white)

    Examples:
        Sets a new NumberToken to display the score.::
            
            self.score = NumberToken(position = (0, 0) number=0)
        
        Gets the number stored in the NumberToken::

            number = self.score.get_number()
        
        Sets the number stored in the NumberToken::

            self.score.set_number(3)
        
    """

    def __init__(self, position=(0, 0), number=0, font_size=80, color=(255, 255, 255, 255)):
        super().__init__(position, str(number), font_size, color)
        self.set_number(number)
        self.is_static = True

    def inc(self):
        """
        Increases the number by one
        """
        self.number += 1
        self.set_text(str(self.number))

    def set_number(self, number):
        """
        Sets the number

        Args:
            number: The number which should be displayed

        Examples:
            
            Sets the number stored in the NumberToken::
            
                self.number_token.set_number(3)
            
        """
        self.number = number
        self.set_text(str(self.number))

    def get_number(self) -> int:
        """

        Returns:
            The current number

        Examples:
            
            Gets the number stored in the NumberToken::
            
                number = self.number_token.get_number()
            
        """
        self.costume.call_action("text changed")
        return int(self.costume.text)
