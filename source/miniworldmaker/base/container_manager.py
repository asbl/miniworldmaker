from typing import List

import miniworldmaker.base.app as app
import miniworldmaker.containers.container as container_mod
from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError


class ContainerManager:
    def __init__(self, miniworldmaker_app: "app.App"):
        self.containers: List["container_mod.Container"] = []
        self.total_width: int = 0
        self.total_height: int = 0
        self.app: "app.App" = miniworldmaker_app
        self.topleft = None

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        """Gets container by pixel coordinates."""
        for container in self.containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container
        return None

    def reload_containers(self):
        """Called in mainloop, triggered 1/frame.

        If dirty, containers are updated and repainted.
        """
        for ct in self.containers:
            if ct.dirty:
                ct.update()
                ct.repaint()
                ct.blit_surface_to_window_surface()

    def add_topleft(self, new_container: "container_mod.Container") -> "container_mod.Container":
        """Adds the topleft corner if it does not exist."""
        for container in self.containers:
            if container.docking_position == "top_left":
                return self.get_topleft()
        self.topleft = new_container
        self.add_container(new_container, "top_left")
        return new_container

    def add_container(self, container: "container_mod.Container", dock: str,
                      size: int = None) -> "container_mod.Container":
        """Adds a new container

        Args:
            container (container.Container): The container
            dock (str): The position: "top_left", "right" or "bottom"
            size (int, optional): Size in pixels. Defaults to attribute `default_size`of container

        Raises:
            MiniworldMakerError: Raises error if container is already in board containers.

        Returns:
            container.Container: The container
        """
        
        if container not in self.containers:
            self.app.window.recalculate_dimensions()
            container.docking_position = dock
            self.containers.append(container)
            if size is None:
                size = container.default_size
            container.add_to_window(self.app, dock, size)
            self.app.window.resize()
            for ct in self.containers:
                ct.dirty = 1
            for board in self.app.running_boards:
                for token in board.tokens:
                    token.dirty = 1
        else:
            raise MiniworldMakerError("Container already in board.containers")
        return container

    def switch_board(self, new_board):
        old_board = self.app.running_board
        app.App.running_boards.remove(old_board)
        app.App.running_board = new_board
        app.App.running_boards.append(new_board)
        new_board._app = old_board._app

        self.app.image = new_board.image
        self.switch_container(old_board, new_board)
        for container in self.containers:
            if container != new_board:
                self.remove_container(container)
        self.app.prepare_mainloop()

    def switch_container(self, container: "container_mod.Container",
                         new_container: "container_mod.Container") -> "container_mod.Container":
        """Switches a container (e.g. replace a board with another board)

        Args:
            container: The container which should be replaced
            new_container: The container which should be inserted
        """
        for i, ct in enumerate(self.containers):
            if ct == container:
                dock = container.docking_position
                self.containers[i] = new_container
                new_container.docking_position = dock
                if dock == "top_left":
                    self.topleft = new_container
                break
        self.update_containers()
        self.app.window.resize()
        return new_container

    def get_topleft(self) -> "container_mod.Container":
        for container in self.containers:
            if container.docking_position == "top_left":
                return container
        raise MiniworldMakerError("Container top_left is missing!")

    def containers_right(self):
        """List of all containers with docking_position "right", ordered by display-position
        """
        return [self.topleft] + [ct for ct in self.containers if ct.docking_position == "right"]

    def containers_bottom(self):
        """List of all containers with docking_position "bottom", ordered by display-position
        """
        return [self.topleft] + [ct for ct in self.containers if ct.docking_position == "bottom"]

    def remove_container(self, container):
        """Removes a container and updates window.
        """
        if container in self.containers:
            self.containers.remove(container)
        for ct in self.containers:
            ct.dirty = 1
        self.update_containers()
        self.app.window.resize()

    def update_containers(self):
        """updates container widths and heights if a container was changed"""
        top_left = 0
        for ct in self.containers_right():
            if ct:
                ct.container_top_left_x = top_left
                top_left += ct.container_width
        top_left = 0
        for ct in self.containers_bottom():
            if ct:
                ct.container_top_left_y = top_left
                top_left += ct.container_height

    def recalculate_containers_width(self) -> int:
        """Recalculates container width
        """
        containers_width: int = 0
        for container in self.containers:
            if container.window_docking_position == "top_left":
                containers_width = container.container_width
            elif container.window_docking_position == "right":
                containers_width += container.container_width
        self.total_width = containers_width
        return containers_width

    def recalculate_containers_height(self) -> int:
        """Recalculates container height"""
        containers_height = 0
        for container in self.containers:
            if container.window_docking_position == "top_left":
                containers_height = container.container_height
            elif container.window_docking_position == "bottom":
                containers_height += container.container_height
        self.total_height = containers_height
        return containers_height
