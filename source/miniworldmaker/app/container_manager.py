from miniworldmaker.containers import container as container_file
from miniworldmaker.app import app

class ContainerManager():

    def __init__(self, miniworldmaker_app: "app.App"):
        self.containers : list = []
        self.containers_right : list = []
        self.containers_bottom : list = []
        self.total_width : int = 0
        self.total_height : int = 0
        self.app : "app.App" = miniworldmaker_app

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self.containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container
        return None

    def reload_containers(self):
        for ct in self.containers:
            if ct.dirty:
                ct.update()
                ct.repaint()
                ct.blit_surface_to_window_surface()

    def add_container(self, container, dock, size=None) -> container_file.Container:
        self.app.window.recalculate_dimensions()
        if dock == "right" or dock == "top_left":
            self.containers_right.append(container)
        if dock == "bottom" or dock == "top_left":
            self.containers_bottom.append(container)
        self.containers.append(container)
        if size is None:
            size = container.default_size
        container._add_to_window(self.app, dock, size)
        self.app.window.recalculate_dimensions()
        self.app.window.display_update()
        self.app.window.dirty = 1
        for ct in self.containers:
            ct.dirty = 1
        if self.app.board:
            for token in self.app.board.tokens:
                token.dirty = 1
        return container

    def remove_container(self, container):
        self.containers.remove(container)
        if container in self.containers_right:
            self.containers_right.remove(container)
        if container in self.containers_bottom:
            self.containers_bottom.remove(container)
        #self._display_update()
        self.app.window.dirty = 1
        for ct in self.containers:
            ct.dirty = 1
        if self.board:
            for token in self.board._tokens:
                token.dirty = 1
        self.update_containers()
        self.app.window.dirty = 1
        
    def update_containers(self):
        top_left = 0
        for ct in self.containers_right:
            ct.container_top_left_x = top_left
            top_left += ct.container_width
        top_left = 0
        for ct in self.containers_bottom:
            ct.container_top_left_y = top_left
            top_left += ct.container_height
        self.app.window.dirty = 1


    def recalculate_containers_width(self) -> int:    
        containers_width : int  = 0
        for container in self.containers:
            if container.window_docking_position == "top_left":
                containers_width = container.container_width
            elif container.window_docking_position == "right":
                containers_width += container.container_width
            elif container.window_docking_position == "main":
                containers_width = container.container_width
        self.total_width = containers_width
        return containers_width
        
    def recalculate_containers_height(self) -> int:
        containers_height = 0
        for container in self.containers:
            if container.window_docking_position == "top_left":
                containers_height = container.container_height
            elif container.window_docking_position == "bottom":
                containers_height += container.container_height
            elif container.window_docking_position == "main":
                containers_height = container.container_height
        self.total_height = containers_height
        return containers_height