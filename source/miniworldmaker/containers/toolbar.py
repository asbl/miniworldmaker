from multiprocessing.sharedctypes import Value
import pygame
from typing import Union, List
from collections import OrderedDict
import itertools

import miniworldmaker.base.app as app
import miniworldmaker.containers.container as container
import miniworldmaker.containers.widgets as widgets


class Toolbar(container.Container):
    """A Toolbar contains widgets (Buttons, Labels, ...)"""

    def __init__(self):
        """
        Base class for toolbars.

        Example:

            Add a Toolbar which interacts with Tokens on board via messages:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()

                board.add_background("images/galaxy.jpg")

                toolbar = Toolbar()
                button = Button("Start Rocket")
                toolbar.add_widget(button)
                board.add_container(toolbar, "right")

                @board.register
                def on_message(self, message):
                    if message == "Start Rocket":
                        rocket.started = True

                rocket = Token(100, 200)
                rocket.add_costume("images/ship.png")
                rocket.started = False
                rocket.turn_left(90)
                rocket.direction = "up"

                @rocket.register
                def act(self):
                    if self.started:
                            self.move()

                @rocket.register
                def on_sensing_not_on_board(self):
                    self.remove()

                board.run()
        """
        super().__init__()
        self.app = app.App
        self.widgets: OrderedDict["widgets.Widget"] = OrderedDict()
        self.timed_widgets = dict()
        self.position = "right"
        self._margin_top = 10
        self._margin_left = 10
        self._margin_right = 10
        self._background_color = (255, 255, 255, 255)
        self.dirty = 1
        self.repaint_all = True  # if True, the complete toolbar will be repainted
        self._first = 0
        self.max_widgets = 0
        self._pagination = False
        self._pagination_widget = None

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value
        self.repaint_all = True

    @property
    def pagination(self):
        return self._pagination

    @pagination.setter
    def pagination(self, value):
        self._pagination = value

    @property
    def background_color(self):
        """Background color as Tuple, e.g. (255,255,255) for white"""
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
        self.dirty = 1

    @property
    def margin_left(self):
        """Defines left margin"""
        return self._margin_left

    @margin_left.setter
    def margin_left(self, value):
        self._margin_left = value
        self.dirty = 1

    @property
    def margin_right(self):
        """Defines right margin"""
        return self._margin_right

    @margin_right.setter
    def margin_right(self, value):
        self._margin_right = value
        self.dirty = 1

    @property
    def margin_top(self):
        """Defines top margin"""
        return self._margin_top

    @margin_top.setter
    def margin_top(self, value):
        self._margin_top = value
        self.dirty = 1

    def add_widget(
        self,
        widget: widgets.Widget,
        key: str = None,
    ) -> widgets.Widget:
        """Adds a widget to the toolbar

        Args:
            widget : The Widget
            key:A unique key

        Returns:
            widgets.Widget: _description_
        """
        if key is None:
            key = widget.text
        if key in self.widgets:
            i = 0
            while i in self.widgets.keys():
                i += 1
            key = i
        widget.clear()
        widget.parent = self
        self.widgets[key] = widget
        self.dirty = 1
        widget.dirty = 1
        if widget.timed:
            self.timed_widgets[widget.name] = widget
        self.repaint_all = True
        return widget

    def remove_widget(self, item: Union[int, str, "widgets.Widget"]):
        """
        Removes a widget from the toolbar. Warning: Be careful when calling this method in a loop.

        Args:
            key: The key of widget which should be removed
        """
        if type(item) in [int, str]:
            self.widgets.pop(item)
        elif isinstance(item, widgets.Widget):
            search_key = None
            for key, value in self.widgets.items():
                if value == item:
                    search_key = key
            if not search_key:
                raise ValueError(f"{item} not found in Toolbar-Widgets")
            else:
                self.widgets.pop(key)
        else:
            raise TypeError(f"item must be of type [int, str, Widget], found {type(item)}")
        self.dirty = 1
        self.repaint_all = True

    def has_widget(self, key: str):
        """Checks if self.widgets has key

        Args:
            key: The key of widget
        """
        if key in self.widgets:
            return True
        else:
            return False

    def get_widget(self, key: str) -> "widgets.Widget":
        """Gets widget by key

        Returns:
            _type_: _description_
        """
        if key in self.widgets:
            return self.widgets[key]
        else:
            raise TypeError(f"Error: Toolbar widgets does not contain key {key}")

    def remove_all_widgets(self):
        self.widgets = dict()
        self.dirty = 1
        self.repaint_all = True

    def repaint(self):
        if self.dirty:
            self.update_width_and_height()
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(self.background_color)
            self._paint_widgets()
        if self.repaint_all:
            self.app.window.repaint_areas.append(self.rect)
            self.repaint_all = False
        self.dirty = 1  # Always dirty so that timed widgets can run

    def widget_iterator(self) -> list:
        if self.max_widgets == 0:
            return self.widgets.values()
        else:
            if len(self.widgets) > self.first + self.max_widgets:
                last_item = self.first + self.max_widgets
            else:
                last_item = len(self.widgets)
        widgets = itertools.islice(self.widgets.values(), self.first, last_item)
        if self.pagination:
            widgets = [self.pagination] + list(widgets)
        return widgets

    def _paint_widgets(self):
        if self.widgets:
            actual_height = self.margin_top
            for widget in self.widget_iterator():
                actual_height += widget.margin_top
                if widget.dirty == 1:
                    self._set_widget_width(widget)
                    widget._repaint()
                    widget._topleft = (self.rect.left + self.margin_left + widget.margin_left, actual_height)
                    rect = pygame.Rect(widget._topleft[0], widget._topleft[1], widget.width, widget.height)
                    self.app.window.repaint_areas.append(rect)
                self.surface.blit(widget.surface, (self.margin_left + widget.margin_left, actual_height))
                actual_height += widget.height + widget.margin_bottom

    def _widgets_total_height(self):
        height = self.margin_top
        for name, widget in self.widgets.items():
            height += widget.margin_top
            height += widget.height + widget.margin_bottom
        return height

    def get_event(self, event, data):
        if event == "mouse_left":
            widget = self.get_widget_by_position(data)
            if widget:
                return widget.on_mouse_left(data)

    def _set_widget_width(self, widget):
        widget._width = (
            self._container_width - self.margin_left - self.margin_right - widget.margin_left - widget.margin_right
        )
        if widget._width < 0:
            widget._width = 0

    def get_widget_by_position(self, pos):
        actual_height = self.margin_top
        local_pos = self.get_local_position(pos)
        if not self.position_is_in_container(pos) or local_pos[1] > self._widgets_total_height():
            return None
        # y pos
        for widget in self.widget_iterator():
            if actual_height + widget.margin_top < local_pos[1] < actual_height + widget.margin_top + widget.height:
                # x pos
                self._set_widget_width(widget)
                internal_x = local_pos[0]
                if (
                    self.margin_left + widget.margin_left
                    < internal_x
                    < self.margin_left + widget.margin_left + widget.width
                ):
                    return widget
                else:
                    return None
            actual_height += widget.margin_bottom + widget.height + widget.margin_top

    def update(self):
        for widget in self.timed_widgets:
            widget.update()

    def send_message(self, text):
        self.app.app.event_manager.send_event_to_containers("message", text)
