import miniworldmaker.boards.board_templates.toolbar.toolbar as toolbar
import miniworldmaker.tokens.token_plugins.widgets.label as label


class Console(toolbar.Toolbar):
    """
    A console.

    You can write text into the console
    """

    def __init__(self):
        super().__init__()
        self.max_lines = 2
        self.text_size = 13
        self.row_margin = 5
        self.rows = (self.max_lines) * (self.row_height + self.row_margin) + self.padding_top + self.padding_bottom

    def newline(self, text):
        self.add_widget(label.Label(text))
        if len(self.widgets) > self.max_widgets:
            self.first += 1

    def add_widget(self, widget: "widget.ButtonWidget", key: str = None, ) -> "widget.ButtonWidget":
        widget.margin_bottom = self.row_margin
        widget.margin_top = 0
        super().add_widget(widget, key)
        if self.pagination and self.pager:
            self.pager.stick()
        return widget
