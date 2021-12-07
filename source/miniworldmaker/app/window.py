import pygame
from miniworldmaker.app import container_manager
from miniworldmaker.app import event_manager

import os


class Window:

    def __init__(self, title, container_manager: "container_manager.ContainerManager", event_manager: "event_manager.EventManager"):
        self.title: str = title
        self.container_manager: "container_manager.ContainerManager" = container_manager
        self.event_manager: "event_manager.EventManager" = event_manager
        self.default_size: int = 200
        self.dirty: int = 1
        self.repaint_areas = []
        self.surface: pygame.Surface = None
        self.full_screen: bool = False
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, "../resources/logo_small_32.png")
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except Exception as e:
            print("Error on creating window: " + str(e))

    def update(self):
        if self.dirty:
            self.display_update()
            self.dirty = False
        self.reload_repaint_areas()
        self.event_manager.handle_event_queue()
        self.container_manager.reload_containers()
        self.dirty = False

    def display_repaint(self):
        pygame.display.update(self.repaint_areas)
        self.repaint_areas = []

    def display_update(self):
        if self.full_screen:
            self.surface = pygame.display.set_mode((self.width, self.height, ), pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.set_alpha(None)

    def reload_repaint_areas(self):
        self.repaint_areas = []
        if self.dirty:
            self.repaint_areas.append(pygame.Rect(0, 0, self.width, self.height))
            self.dirty = 0

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
