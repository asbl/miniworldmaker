import miniworldmaker.tokens.token_plugins.widgets.buttonwidget as widget
class CounterLabel(widget.ButtonWidget):
    """A counter label contains a `description` and a `counter`. The counter starts with value 0 and can be modified with
    `add` and `sub`
    """

    def __init__(self, description, img_path=None):
        super().__init__()
        if img_path:
            self.set_image(img_path)
        self.value = 0
        self.description = description
        self.set_text("{0} : {1}".format(self.description, str(self.value)))
        self.data = str(0)

    def add(self, value):
        self.value += value
        self.update_text()

    def sub(self, value):
        self.value -= value
        self.update_text()

    def get_value(self):
        return self.value

    def set(self, value):
        self.value = value
        self.update_text()

    def update_text(self):
        self.set_text("{0} : {1}".format(self.description, str(self.value)))