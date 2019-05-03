from miniworldmaker.tokens import text_token

class NumberToken(text_token.TextToken):

    def __init__(self, number, position):
        super().__init__(str(number), position)
        self.number = number

    def inc(self):
        self.number+= 1
        self.set_text(str(self.number))

    def get_text(self):
        return self.costume.text