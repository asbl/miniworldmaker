import miniworldmaker.tokens.token_plugins.widgets.buttonwidget as widget
class FPSLabel(widget.ButtonWidget):
    def __init__(self, board, text, img_path=None):
        super().__init__()
        if img_path:
            self.set_image(img_path)
        self.board = board
        self.value = self.board.clock.get_fps()
        self.text = text
        self.set_text("{0} : {1}".format(self.text, str(self.value)))
        self.data = str(0)
        self.timed = True

    def update(self):
        self.value = self.board.clock.get_fps()
        self.set_text("{0} : {1}".format(self.text, str(self.value)))