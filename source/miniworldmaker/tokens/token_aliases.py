class TokenAliases:
    @property
    def color(self):
        """->See :py:attr:`Token.fill_color`"""
        return self.costume.fill_color

    @color.setter
    def color(self, value):
        self.fill_color = value

    @property
    def stroke_color(self):
        """see :py:attr:`Token.border_color`"""
        return self.border_color

    @stroke_color.setter
    def stroke_color(self, value):
        self.border_color = value
