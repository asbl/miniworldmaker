import os

import pygame

import miniworldmaker.base.container_manager as container_manager_mod
import miniworldmaker.base.app_event_manager as event_manager_mod


class Window:

    def __init__(self, title, container_manager: "container_manager_mod.ContainerManager",
                 event_manager: "event_manager_mod.AppEventManager"):
        self._containers_height = None
        self._containers_width = None
        self.title: str = title
        self.container_manager: "container_manager_mod.ContainerManager" = container_manager
        self.event_manager: "event_manager_mod.AppEventManager" = event_manager
        self.default_size: int = 200
        self.dirty: int = 1
        self.repaint_areas = []
        self._surface: pygame.Surface = pygame.Surface((0, 0))
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
            raise Exception("Error on creating window: " + str(e))

    @property
    def fullscreen(self):
        """toggles fullscreen mode
        """
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        self._fullscreen = value
        self.update_surface()

    @property
    def fit_desktop(self):
        return self._fit_desktop

    @fit_desktop.setter
    def fit_desktop(self, value):
        """fits to desktop
        """
        self._fit_desktop = value
        self.dirty = 1
        # self.display_update()

    @property
    def replit(self):
        """Scales display to 800x600 for replit
        """
        return self._replit

    @replit.setter
    def replit(self, value):
        self._replit = value
        self.dirty = 1
        # self.display_update()

    def display_repaint(self):
        """Called 1/frame - Draws all repaint rects and resets the repaint areas.
        """
        pygame.display.update(self.repaint_areas)
        self.repaint_areas = []

    @property
    def surface(self):
        return self._surface

    def update_surface(self):
        """Updates the surface of window. Everything is drawn and scaled to the surface
        
        Defaults to containers_width/height
        
        Depends on the values of self.fullscreen, self.fit_desktop and self.replit
        """
        if self.fullscreen:
            self._surface = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
            pygame.display.toggle_fullscreen()
        elif self.fit_desktop:
            self._surface = pygame.display.set_mode((0, 0))
        elif self.replit:
            self._surface = pygame.display.set_mode((800, 600), pygame.SCALED)
        else:
            info = pygame.display.Info()
            x, y = max((info.current_w - self.width) / 2, 0), max((info.current_h - self.height) / 2, 0)
            os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x, y)
            self._surface = pygame.display.set_mode((self.width, self.height))
        self._surface.set_alpha(None)

    def display_update(self):
        """Updates the display
        @todo: Can be merged into display_repaint and update_surface
        """
        if self.dirty:
            self.dirty = 0
            self.add_display_to_repaint_areas()
            pygame.display.update(self.repaint_areas)
            self.repaint_areas = []

    def add_display_to_repaint_areas(self):
        self.repaint_areas.append(pygame.Rect(0, 0, self.width, self.height))

    def recalculate_dimensions(self):
        """Updates container sizes and recalculates dimensions"""
        self.container_manager.update_containers()
        containers_width = self.container_manager.recalculate_containers_width()
        containers_height = self.container_manager.recalculate_containers_height()
        self.dirty = 1
        self.repaint_areas.append(pygame.Rect(0, 0, self.width, self.height))
        self._containers_width, self._containers_height = containers_width, containers_height

    @property
    def width(self) -> int:
        """Gets total width from container manager
        """
        return self.container_manager.total_width

    @property
    def height(self) -> int:
        """Gets total height from container manager
        """
        return self.container_manager.total_height

    def resize(self):
        """Resizes the window:
        1. Recalculates the container dimensions
        2. updates own surface
        3. updates display
        """
        self.recalculate_dimensions()
        self.update_surface()
        self.display_update()
