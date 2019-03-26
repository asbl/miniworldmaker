from miniworldmaker.containers.container import Container
from miniworldmaker.containers.toolbar_widgets import ToolbarWidget

class Toolbar(Container):

    def __init__(self, size=150):
        super().__init__(size)
        self.widgets = []
        self.position = "right"
        self.margin_first = 10
        self.margin_last = 5
        self.row_height = 25
        self.row_margin = 4
        self.margin_left = 10
        self.margin_right = 10
        self.dirty = 1

    def get_widget(self, index):
        return self.widgets[index]

    def add_widget(self, widget) -> ToolbarWidget:
        """
        adds a widget to the toolbar
        :param widget: A toolbar widget
        :return:
        """
        widget.clear()
        widget.parent = self
        self.widgets.append(widget)
        return widget

    def repaint(self):
        if self.dirty:
            self.surface.fill((255, 255, 255))
            if self.widgets:
                height = self.margin_first
                for widget in self.widgets:
                    if widget.dirty == 1:
                        widget.width = self._container_width - self.margin_left - self.margin_right
                        widget.height = self.row_height
                        widget.repaint()
                        self.surface.blit(widget.surface, (5, height))
                        widget.dirty = 0
                    height += widget.height + self.row_margin
                self.dirty = 0
                self._window.repaint_areas.append(self.rect)

    def _widgets_total_height(self):
        height = self.margin_first
        for widget in self.widgets:
            height += widget.height
        return height

    def get_event(self, event, data):
        if event == "mouse_left":
            height = self.margin_first
            x, y = data[0], data[1]
            if not y > self._widgets_total_height():
                for widget in self.widgets:
                    if height + widget.height > y:
                        return widget.get_event(event, data)
                    else:
                        height = height + widget.height + self.row_margin
        else:
            return "no toolbar event"
