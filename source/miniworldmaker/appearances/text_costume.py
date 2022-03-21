from miniworldmaker.appearances import costume


class TextCostume(costume.Costume):
    def __init__(self, token):
        super().__init__(token)
        self.set_image((0, 0, 0, 0))
        self.fill_color = (255, 255, 255, 255)
