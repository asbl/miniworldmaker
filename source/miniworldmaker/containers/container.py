import logging

import pygame


class Container:
    clog = logging.getLogger("Container")

    def __init__(self, size=0):
        self.dirty = 1
        self.background_color = (255, 255, 255)
        self.size = size
        self.listen_to_all_events = False
        # private
        self._window = None  # Set in add_to_window
        self._container_width = 0  # Set in add_to_window
        self._container_height = 0  # Set in add_to_window
        self._container_top_left_x = 0  # Set in add_to_window
        self._container_top_left_y = 0  # Set in add_to_window
        self._docking_position = None  # Set in add_to_windows
        self._image = None

    @property
    def window(self):
        return self._window

    def _add_to_window(self, window, dock, size=None):
        self._window = window
        if size != None:
            self.size = size
        if dock == "main":
            self._docking_position = dock
        if dock == "top_left":
            self._container_top_left_x = 0
            self._container_top_left_y = 0
            self._docking_position = dock
            self._container_height = self._window.window_height
            self._container_width = self.size
        elif dock == "right":
            self._container_top_left_x = self._window.window_width
            self._container_top_left_y = 0
            self._docking_position = dock
            self._container_height = self._window.window_height
            self._container_width = self.size
        elif dock == "bottom":
            self._container_top_left_x = 0
            self._container_top_left_y = self._window.window_height
            self._docking_position = dock
            self._container_width = self._window.window_width
            self._container_height = self.size
        self.clog.info("Added Container {0} with width: {1} and height {2}".format(self, self.width, self.height))
        self._image = pygame.Surface((self.width, self.height))

    def repaint(self):
        pass

    def blit_surface_to_window_surface(self):
        self._window.window_surface.blit(self._image, self.rect)

    def remove(self):
        pass

    def pass_event(self, event, data):
        pass

    def get_event(self, event, data):
        pass

    @property
    def surface(self):
        return self._image

    @property
    def rect(self):
        return pygame.Rect(self._container_top_left_x, self._container_top_left_y, self.width, self.height)

    @property
    def window_docking_position(self):
        return self._docking_position

    def update(self):
        pass

    @property
    def width(self):
        return self._container_width

    @property
    def height(self):
        return self._container_height
