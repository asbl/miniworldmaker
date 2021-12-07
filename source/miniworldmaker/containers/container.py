import pygame

class Container:
    """
    Base class for containers
    """

    def __init__(self):
        self.dirty = 1
        self.surface = pygame.Surface((1, 1))
        self.background_color = (255, 255, 255)
        self.default_size = 100
        self.container_size = self.default_size
        self.registered_events = {"mouse_left", "mouse_right"}
        # private
        self._window = None  # Set in add_to_window
        self._app = None
        self._container_width = 0  # Set in add_to_window
        self._container_height = 0  # Set in add_to_window
        self.container_top_left_x = 0  # Set in add_to_window
        self.container_top_left_y = 0  # Set in add_to_window
        self.docking_position = None  # Set in add_to_windows
        self._image = None

    @property
    def container_width(self):
        return self._container_width

    @property
    def container_height(self):
        return self._container_height

    @property
    def window(self):
        return self._window

    def _add_to_window(self, app, dock, size=None):
        self._app = app
        if size== None:
            self.container_size = self.default_size
        else:
            self.container_size = size
        self.docking_position = dock
        self.update_width_and_height()
        self._image = pygame.Surface((self.width, self.height))

    def update_width_and_height(self):
        if self.docking_position == "top_left":
            self.container_top_left_x = 0
            self.container_top_left_y = 0     
        elif self.docking_position == "right":
            self.container_top_left_y = 0
            self._container_height = self._app.window.height
            self._container_width = self.container_size
        elif self.docking_position == "bottom":
            self.container_top_left_x = 0
            self._container_width = self._app.window.width
            self._container_height = self.container_size

    @property
    def size(self):
        return self._container_width, self._container_height

    def repaint(self):
        """ 
        Implemented in subclasses
        """
        pass

    def blit_surface_to_window_surface(self):
        self._app.window.surface.blit(self.surface, self.rect)

    def remove(self):
        """ 
        Implemented in subclasses
        """
        pass

    def handle_event(self, event, data):
        self.get_event(event, data)

    def get_event(self, event, data):
        """ 
        Implemented in subclasses
        """
        pass

    def is_in_container(self, x, y):
        if self.rect.collidepoint((x, y)):
            return True
        else:
            return False

    @property
    def rect(self):
        return pygame.Rect(self.container_top_left_x, self.container_top_left_y, self.width, self.height)

    @property
    def window_docking_position(self):
        return self.docking_position

    def update(self):
        """ 
        Implemented in subclasses
        """
        pass

    @property
    def width(self):
        return self._container_width

    @property
    def height(self):
        return self._container_height