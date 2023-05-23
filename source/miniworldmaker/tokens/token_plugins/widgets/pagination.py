import miniworldmaker.tokens.token_plugins.widgets.button as button
import miniworldmaker.tokens.token_plugins.widgets.container_widget as container_widget


class Pager(container_widget.ContainerWidget):
    def __init__(self, up_text="up", down_text="down", ):
        self.up = button.Button(up_text)
        self.up.parent = self
        self.down = button.Button(down_text)
        self.down.parent = self
        super().__init__([self.up, self.down])
        self.scroll_steps = 10
        # needed for decorators
        up = self.up
        down = self.down
        self.row_height = 60
        self.sticky = True
        
        for child in self.children:
            child.set_background_color((20, 20, 20, 230))

        @up.register
        def on_pressed_left(self, pos):
            self.board.scroll_up(self.parent.scroll_steps)
            self.parent.stick()

        @down.register
        def on_pressed_left(self, pos):
            self.board.scroll_down(self.parent.scroll_steps)
            self.parent.stick()

    def on_setup(self):
        self.layer = 10
        
    def on_clicked_left(self, pos):
        self.stick()

    def stick(self):
        self.y = (self.board.camera.y + self.board.padding_top)
        if not self.board.can_scroll_down(self.scroll_steps):
            self.down.visible = False
        else:
            self.down.visible = True
        if not self.board.can_scroll_up(self.scroll_steps):
            self.up.visible = False
        else:
            self.up.visible = True