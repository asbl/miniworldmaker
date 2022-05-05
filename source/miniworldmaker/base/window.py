import pygame
import os

import miniworldmaker.base.container_manager as container_manager
import miniworldmaker.base.event_manager as event_manager


class Window:

    def __init__(self, title, container_manager: "container_manager.ContainerManager",
                 event_manager: "event_manager.EventManager"):
        self.title: str = title
        self.container_manager: "container_manager.ContainerManager" = container_manager
        self.event_manager: "event_manager.EventManager" = event_manager
        self.default_size: int = 200
        self.dirty: int = 1
        self.repaint_areas = []
        self._surface: pygame.Surface = None
        self._fullscreen: bool = False
        self._fit_desktop = False
        self._replit = False
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, "../resources/logo_small_32.png")
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except Exception as e:
            print("Error on creating window: " + str(e))

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        self._fullscreen = value
        self.dirty = 1
        # self.display_update()

    @property
    def fit_desktop(self):
        return self._fit_desktop

    @fit_desktop.setter
    def fit_desktop(self, value):
        self._fit_desktop = value
        self.dirty = 1
        # self.display_update()

    @property
    def replit(self):
        return self._replit

    @replit.setter
    def replit(self, value):
        self._replit = value
        self.dirty = 1
        # self.display_update()

    def display_repaint(self):
        pygame.display.update(self.repaint_areas)
        self.reset_repaint_areas()

    @property
    def surface(self):
        if self.dirty or self._surface == None:
            self.update_surface()
        return self._surface

    def update_surface(self):
        if self.fullscreen:
            self._surface = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
        elif self.fit_desktop:
            self._surface = pygame.display.set_mode((0, 0))
        elif self.replit:
            self._surface = pygame.display.set_mode((800, 600), pygame.SCALED)
        else:
            self._surface = pygame.display.set_mode((self.width, self.height))
        self._surface.set_alpha(None)

    def display_update(self):
        if self.dirty:
            self.update_surface()
            if self.fullscreen:
                pygame.display.toggle_fullscreen()
            self.add_display_to_repaint_areas()
            pygame.display.flip()
        self.dirty = 0

    def reset_repaint_areas(self):
        self.repaint_areas = []

    def add_display_to_repaint_areas(self):
        self.repaint_areas.append(pygame.Rect(0, 0, self.width, self.height))

    def recalculate_dimensions(self):
        self.container_manager.update_containers()
        containers_width = self.container_manager.recalculate_containers_width()
        containers_height = self.container_manager.recalculate_containers_height()
        self.dirty = 1
        self.repaint_areas.append(pygame.Rect(0, 0, self.width, self.height))
        self._containers_width, self._containers_height = containers_width, containers_height

    @property
    def width(self) -> int:
        return self.container_manager.total_width

    @property
    def height(self) -> int:
        return self.container_manager.total_height
