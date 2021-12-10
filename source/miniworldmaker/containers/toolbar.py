import pygame
from miniworldmaker.containers import container
from miniworldmaker.containers import toolbar_widgets
from miniworldmaker.app import app
import miniworldmaker

class Toolbar(container.Container):

    def __init__(self):
        """
        Base class for toolbars.
        """
        super().__init__()
        self.app = miniworldmaker.App
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
        self.repaint_all = True

    def get_widget(self, index):
        return self.widgets[index]

    def add_widget(self, widget: toolbar_widgets.ToolbarWidget) -> toolbar_widgets.ToolbarWidget:
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
        self.repaint_all = True
        return widget

    def remove_widget(self, widget):
        """
        Removes a widget from the toolbar. Warning: Be careful when calling this method in a loop.

        Args:
            widget: The widget which should be removed
        """
        self.widgets.remove(widget)
        self.dirty = 1
        self.repaint_all = True

    def remove_all_widgets(self):
        self.widgets = []
        self.dirty = 1
        self.repaint_all = True

    def repaint(self):
        if self.dirty:
            self.update_width_and_height()
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill((255, 255, 255, 255))
            if self.widgets:
                actual_height = self.margin_first
                for widget in self.widgets:
                    if widget.dirty == 1:
                        widget.width = self._container_width - self.margin_left - self.margin_right
                        widget.repaint()
                        rect = pygame.Rect(self.rect.left, actual_height,
                                           widget.width, widget.height)
                        self.app.window.repaint_areas.append(rect)
                    self.surface.blit(widget.surface, (5, actual_height))
                    actual_height += widget.height + self.row_margin
        if self.repaint_all:
            self.app.window.repaint_areas.append(self.rect)
            self.repaint_all = False
        self.dirty = 1  # Always dirty so that timed widgets can run

    def _widgets_total_height(self):
        height = self.margin_first
        for widget in self.widgets:
            height += widget.height + self.row_margin
        return height

    def get_event(self, event, data):
        if event == "mouse_left":
            height = self.margin_first
            x, y = data[0], data[1]
            if self.is_in_container(x, y) and not y > self._widgets_total_height():
                for widget in self.widgets:
                    if height + widget.height > y:
                        return widget.get_event(event, data)
                    else:
                        height = height + widget.height + self.row_margin

    def update(self):
        for widget in self.timed_widgets:
            widget.update()
