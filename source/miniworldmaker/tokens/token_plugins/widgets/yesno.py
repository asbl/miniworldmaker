import miniworldmaker.tokens.token_plugins.widgets.button as button
import miniworldmaker.tokens.token_plugins.widgets.container_widget as container_widget


class YesNoButton(container_widget.ContainerWidget):

    def __init__(self, yes_text, no_text):
        self.yes = button.Button(yes_text)
        self.no = button.Button(no_text)
        super().__init__([self.yes, self.no])
        self.row_height = 80

    def get_yes_button(self):
        return self.yes

    def get_no_button(self):
        return self.no