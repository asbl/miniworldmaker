import os
import pygame
from miniworldmaker.containers.container import Container
from miniworldmaker.containers.console import Console


class EventConsole(Console):

    event_id = 0

    def __init__(self):
        super().__init__()
        self.register_events.add("all")

    def get_event(self, event, data):
        text = "Nr: {0}, Event: {1}, Data: {2}".format(self.event_id, str(event), str(data))
        self.event_id += 1
        self._text_queue.append(text)
        if len(self._text_queue) > self.lines:
            self._text_queue.pop(0)
        self.dirty = 1
