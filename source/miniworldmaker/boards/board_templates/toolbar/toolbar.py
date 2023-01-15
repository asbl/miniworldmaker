from collections import OrderedDict
from typing import Union

import miniworldmaker.base.app as app_mod
import miniworldmaker.boards.board_templates.pixel_board.board as board
import miniworldmaker.tokens.token_plugins.widgets.pagination as pagination
import miniworldmaker.tokens.token_plugins.widgets.widget_base as widget_base


class Toolbar(board.Board):
    """A Toolbar contains widgets (Buttopaginationns, Labels, ...)"""

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
                def on_sensing_not_on_the_board(self):
                    self.remove()

                board.run()
        """
        super().__init__()
        self.widgets: OrderedDict["widget_base.BaseWidget"] = OrderedDict()
        self.timed_widgets = dict()
        self.position = "right"
        self._padding_top = 10
        self._padding_bottom = 0
        self._padding_left = 10
        self._padding_right = 10
        self.row_height = 26
        self._background_color = (255, 255, 255, 255)
        self._first = 0
        self.max_widgets = 0
        self.max_row_height = 0
        self._pagination = False
        self.pager = None

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value
        self.reorder()

    def on_change(self):
        if hasattr(self, "widgets"):
            for widget in self.widgets.values():
                widget.width = self.width
        self.reorder()

    @property
    def pagination(self):
        return self._pagination

    @pagination.setter
    def pagination(self, value):
        if value:
            self._pagination = True
            self.pager = self.add_widget(pagination.Pager())

    @property
    def background_color(self):
        """Background color as Tuple, e.g. (255,255,255) for white"""
        return self.background

    @background_color.setter
    def background_color(self, value):
        self.set_background(value)

    @property
    def padding_left(self):
        """Defines left margin"""
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value):
        self._padding_left = value
        self.dirty = 1

    @property
    def padding_right(self):
        """Defines right margin"""
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value):
        self._padding_right = value
        self.dirty = 1

    @property
    def padding_top(self):
        """Defines top margin"""
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value):
        self._padding_top = value
        self.dirty = 1

    @property
    def padding_bottom(self):
        """Defines bottom margin"""
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        self._padding_bottom = value
        self.dirty = 1

    def add_widget(self, widget: "widget_base.BaseWidget", key: str = None, ) -> "widget_base.BaseWidget":
        """Adds a widget to the toolbar

        Args:
            widget : The Widget
            key:A unique key

        Returns:
            widgets.Widget: _description_
        """
        widget.board = self
        widget.width = self.width  # set to full board width
        widget.row_height = self.row_height
        widget.parent = self
        if key is None:
            key = widget.value
        if key in self.widgets:
            i = 0
            while i in self.widgets.keys():
                i += 1
            key = i
        self.widgets[key] = widget
        if widget.timed:
            self.timed_widgets[widget.name] = widget
        widget.resize()
        """ Set position
        """
        self.reorder()
        if widget.y + widget.height > self.camera.y + self.container_height:
            self.camera.boundary_y = widget.y + widget.height
            self.camera.y = widget.y + widget.height - self.container_height
        return widget

    def remove_widget(self, item: Union[int, str, "widget_base.BaseWidget"]):
        """
        Removes a widget from the toolbar. Warning: Be careful when calling this method in a loop.

        Args:
            key: The key of widget which should be removed
        """
        if type(item) in [int, str]:
            self.widgets.pop(item)
        elif isinstance(item, widget_base.BaseWidget):
            search_key = None
            for key, value in self.widgets.items():
                if value == item:
                    search_key = key
            if not search_key:
                raise ValueError(f"{item} not found in Toolbar-Widgets")
            else:
                self.widgets.pop(key)
                value.remove()
        else:
            raise TypeError(f"item must be of type [int, str, Widget], found {type(item)}")

    def has_widget(self, key: str):
        """Checks if self.widgets has key

        Args:
            key: The key of widget
        """
        if key in self.widgets:
            return True
        else:
            return False

    def get_widget(self, key: str) -> "widget_base.BaseWidget":
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

    def reorder(self):
        self.update_width_and_height()
        if hasattr(self, "widgets") and self.widgets:
            actual_height = self.padding_top
            for widget in self.widgets.values():
                if widget.sticky:
                    widget.stick()
                else:
                    actual_height += widget.margin_top
                    self._set_widget_width(widget)
                    widget.topleft = (self.padding_left + widget.margin_left, actual_height)
                    if self.max_row_height != 0:
                        widget.height = self.max_row_height
                    actual_height += widget.height + widget.margin_bottom

    """def widget_iterator(self) -> list:
        ""Iteration with pagination
        ""
        if self.max_widgets == 0:
            return self.widgets.values()
        else:
            if len(self.widgets) > self.first + self.max_widgets:
                last_item = self.first + self.max_widgets
            else:
                last_item = len(self.widgets)
        widgets = itertools.islice(self.widgets.values(), self.first, last_item)
        return widgets
    """

    def _widgets_total_height(self):
        height = self.padding_top
        for name, widget in self.widgets.items():
            height += widget.margin_top
            height += widget.height + widget.margin_bottom
        return height

    def _set_widget_width(self, widget):
        new_width = self.container_width - self.padding_left - self.padding_right - widget.margin_left - widget.margin_right
        if new_width < 0:
            new_width = 0
        widget.width = new_width

    def update_width_and_height(self):
        super().container_width

    def update(self):
        super().update()
        for widget in self.timed_widgets:
            widget.update()

    def send_message(self, text):
        app_mod.App.running_app.event_manager.to_event_queue("message", text)

    def scroll_up(self, value):
        if self.can_scroll_up(value):
            self.camera_y -= value
            self.camera_y = max(0, self.camera_y)
            for key, widget in self.widgets.items():
                widget.resize()

    def scroll_down(self, value):
        if self.can_scroll_down(value):
            self.camera_y += value
            for key, widget in self.widgets.items():
                widget.resize()

    def can_scroll_down(self, value):
        if self.camera_y + value > self.boundary_y - self.viewport_height:
            return False
        else:
            return True

    def can_scroll_up(self, value):
        if self.camera_y == 0:
            return False
        else:
            return True
