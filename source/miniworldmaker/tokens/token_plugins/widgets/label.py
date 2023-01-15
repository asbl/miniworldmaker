import miniworldmaker.tokens.token_plugins.widgets.buttonwidget as widget


class Label(widget.ButtonWidget):
    def __init__(self, text, img_path=None):
        super().__init__()
        if img_path:
            self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text
        self.background_color = (255, 255, 255, 0)


class ToolbarLabel(Label):
    """legacy Code"""
    pass
