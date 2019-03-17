from miniworldmaker.containers.container import Container


class Toolbar(Container):

    def __init__(self, size=100):
        super().__init__(size)
        self.widgets = []
        self.position = "right"
        self.dirty = 1

    def get_widget(self, index):
        return self.widgets[index]

    def add_widget(self, widget):
        """
        adds a widget to the toolbar
        :param widget: A toolbar widget
        :return:
        """
        widget.clear()
        widget.parent = self
        self.widgets.append(widget)

    def repaint(self):
        if self.dirty:
            self.surface.fill((255, 255, 255))
            if self.widgets:
                height = 0
                for widget in self.widgets:
                    if widget.dirty == 1:
                        widget.width = self._container_width
                        widget.height = 30
                        widget.repaint()
                        self.surface.blit(widget.surface, (0, height))
                        widget.dirty = 0
                    height += widget.height
                self.dirty = 0
                self._window.repaint_areas.append(self.rect)

    def _widgets_total_height(self):
        height = 0
        for widget in self.widgets:
            height += widget.height
        return height

    def get_event(self, event, data):
        if event == "mouse_left":
            height = 0
            x, y = data[0], data[1]
            if not y > self._widgets_total_height():
                for widget in self.widgets:
                    if height + widget.height > y:
                        return widget.get_event(event, data)
                    else:
                        height = height + widget.height
        else:
            return "no toolbar event"
