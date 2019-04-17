from miniworldmaker.containers.container import Container
from miniworldmaker.containers import toolbar_widgets
import pygame

class Toolbar(Container):

    def __init__(self):
        super().__init__()
        self.widgets = []
        self.timed_widgets = []
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

    def add_widget(self, widget : toolbar_widgets.ToolbarWidget ) -> toolbar_widgets.ToolbarWidget:
        """
        Adds a widget to the toolbar

        Args:
            widget: the widget which should be added

        Returns: The widget which was added

        """
        widget.clear()
        widget.parent = self
        self.widgets.append(widget)
        widget.height = self.row_height
        self.dirty = 1
        widget.dirty = 1
        if widget.timed:
            self.timed_widgets.append(widget)
        return widget

    def remove_widget(self, widget):
        """
        Removes a widget from the toolbar. Warning: Be careful when calling this method in a loop.

        Args:
            widget: The widget which should be removed
        """
        self.widgets.remove(widget)
        self.dirty = 1

    def remove_all_widgets(self):
        self.widgets = []

    def repaint(self):
        if self.dirty:
            self.surface.fill((255, 255, 255))
            if self.widgets:
                actual_height = self.margin_first
                for widget in self.widgets:
                    if widget.dirty == 1:
                        widget.width = self._container_width - self.margin_left - self.margin_right
                        widget.repaint()
                        rect = pygame.Rect(self.rect.left, actual_height, widget.width, widget.height)
                        self._window.repaint_areas.append(rect)
                    self.surface.blit(widget.surface, (5, actual_height))
                    actual_height += widget.height + self.row_margin
                self.dirty = 0

    def _widgets_total_height(self):
        height = self.margin_first
        for widget in self.widgets:
            height += widget.height + self.row_margin
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

    def update(self):
        for widget in self.timed_widgets:
            widget.update()
