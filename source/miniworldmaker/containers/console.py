import pygame

from miniworldmaker.containers import container
from miniworldmaker.containers import toolbar
from miniworldmaker.containers import widgets

class Console(toolbar.Toolbar):
    """
    A console.

    You can write text into the console
    """
    
    def __init__(self):
        super().__init__()
        self.max_lines = 2

    @property
    def lines(self):
        self._lines = int(self.height - self.margin_first - self.margin_last) / \
            (self.row_height + self.row_margin)
        return self._lines

    def newline(self, text):
        self.add_widget(widgets.Label(text))
        if len(self.widgets) > self.max_widgets:
            self.first +=1

    @property 
    def max_lines(self):
        return self.widgets

    @max_lines.setter
    def max_lines(self, value):
        self.max_widgets = value
        
    def insert(self, widget):
        self.add_widget(widget)
        if len(self.widgets) > self.max_widgets:
            self.first +=1
    