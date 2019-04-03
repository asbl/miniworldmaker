import logging
import os
import pygame
from miniworldmaker.tools import keys
from miniworldmaker.containers.container import Container
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF

class MiniWorldWindow:
    log = logging.getLogger("Window")
    board = None
    window = None

    def __init__(self, title):
        self.title = title
        self._containers = []
        MiniWorldWindow.window = self
        self._quit = False
        self.dirty = 1
        self.repaint_areas = []
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.window_surface.set_alpha(None)
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../resources/logo_small_32.png")
        surface = pygame.image.load(path)
        pygame.display.set_icon(surface)

    def show(self):
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        while not self._quit:
            self.update()
        pygame.quit()

    def update(self):
        self.process_pygame_events()
        self.repaint_areas = []
        if self.dirty:
            self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
            self.dirty = 0
        for container in self._containers:
            container.update()
            container.repaint()
            container.blit_surface_to_window_surface()
        pygame.display.update(self.repaint_areas)
        self.repaint_areas = []

    def add_container(self, container, dock, size=None) -> Container:
        self._containers.append(container)
        container._add_to_window(self, dock, size)
        return container

    def remove_container(self, container):
        self._containers.remove(container)

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self._containers:
            container.remove()
            self.remove_container(container)

    @property
    def window_width(self):
        containers_width = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_width = container.width
            elif container.window_docking_position == "right":
                containers_width += container.width
            elif container.window_docking_position == "main":
                containers_width = container.width
        return containers_width

    @property
    def window_height(self):
        containers_height = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_height = container.height
            elif container.window_docking_position == "bottom":
                containers_height += container.height
            elif container.window_docking_position == "main":
                containers_height = container.height
        return containers_height

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self._containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container
        return None

    def process_pygame_events(self):
        for event in pygame.event.get():
            # Event: Quit
            if event.type == pygame.QUIT:
                self._call_quit_event()
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                container_set = set()
                clicked_container = self.get_container_by_pixel(pos[0], pos[1])
                container_set.add(clicked_container)  # add container which was clicked
                for container in container_set:
                    if event.button == 1:
                        self.send_event_to_containers(container, "mouse_left", (pos[0], pos[1]))
                    if event.button == 3:
                        self.send_event_to_containers(container, "mouse_right", (pos[0], pos[1]))
            elif event.type == pygame.KEYDOWN:
                # key-events
                keys_pressed = pygame.key.get_pressed()
                self.send_event_to_containers("key_down", keys.key_codes_to_keys(keys_pressed))
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
        return False

    def send_event_to_containers(self, event, data):
        self.log.info("Send event '{0}' with data: {1}".format(event, data))
        for container in self._containers:
            if event in container.register_events or "all" in container.register_events:
                container.pass_event(event, data)
                container.get_event(event, data)

    def _call_quit_event(self):
        self._quit = True
        import fileinput
        self._quit = True
