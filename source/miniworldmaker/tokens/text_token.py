from miniworldmaker.tokens import token

class TextToken(token.Token):
    def __init__(self, text):
        super().__init__()
        self.costume.fill_color=(0,0,0,0)
        self.costume.font_size = 80
        self.costume.text = text
        self.costume.is_scaled = True

    def set_text(self, text):
        self.costume.text = text

    def get_text(self):
        return self.costume.text