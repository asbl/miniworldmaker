class TokenAliases:
    @property
    def color(self):
        """->See :py:attr:`Token.fill_color`"""
        return self.costume.fill_color

    @color.setter
    def color(self, value):
        self.costume.fill_color = value