from miniworldmaker.tokens import text_token


class NumberToken(text_token.TextToken):

    def __init__(self, position, number = 0):
        super().__init__(position, str(number))
        self.number = number

    def inc(self):
        self.number+= 1
        self.set_text(str(self.number))

    def set_number(self, number):
        self.number = number
        self.set_text(str(self.number))

    def get_text(self):
        return self.costume.text