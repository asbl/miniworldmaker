import os
import pygame
from miniworldmaker.containers.container import Container
from miniworldmaker.containers.actionbar_widgets import *


class ActionBar(Container):

    def __init__(self, board):
        super().__init__(size=40)
        self.widgets = []
        self.position = "right"
        self.board = board
        self.add_widget(PlayButton(self.board))
        self.add_widget(RunButton(self.board))
        self.add_widget(ResetButton(self.board))
        self.add_widget(InfoButton(self.board))
        self.add_widget(SpeedDownButton(self.board))
        self.add_widget(SpeedLabel(self.board))
        self.add_widget(SpeedUpButton(self.board))
        self.board.is_running = False
        self.dirty = 1

    def add_widget(self, widget):
        """
        adds a widget to the toolbar
        :param widget: A toolbar widget
        :return:
        """
        widget.clear()
        widget.parent = self
        self.widgets.append(widget)
        widget.dirty = 1

    def repaint(self):
        if self.dirty:
            self.surface.fill((255, 255, 255))
            if self.widgets:
                actual_position = 5
                for widget in self.widgets:
                    widget.height = self._container_height - 10
                    widget.repaint()
                    self.surface.blit(widget.surface, (actual_position, 5))
                    actual_position += widget.width + 5  # 5 is padding between elements
                self.dirty = 0
                self._window.repaint_areas.append(self.rect)

    def _widgets_total_width(self):
        width = 0
        for widget in self.widgets:
            width += widget.width + 5
        return width - 5

    def get_event(self, event, data):
        print("actionbar - get event")
        if event == "mouse_left":
            actual_position = 5
            x, y = data[0], data[1]
            if not x > self._widgets_total_width():
                for widget in self.widgets:
                    if actual_position + widget.width + 5 > x:
                        return widget.get_event(event, data)
                    else:
                        actual_position = actual_position + widget.height + 5
        else:
            return "no toolbar event"
