import logging
import os
import sys
from collections import deque

import miniworldmaker.containers.actionbar as a_bar
import pkg_resources
import pygame
from miniworldmaker.containers import color_toolbar
from miniworldmaker.containers import container as container_file
from miniworldmaker.containers import event_console
from miniworldmaker.containers import inspect_actor_toolbar
from miniworldmaker.containers import level_designer_toolbar
from miniworldmaker.tools import keys

version = pkg_resources.require("MiniWorldMaker")[0].version
print("Show new MiniWorldMaker v.{0} Window".format(version))
print("Let's go")


class App:
    """The class app contains the game itself. It's created the first time you call board.show().
    """
    log = logging.getLogger("miniworldmaker")
    board = None
    window = None
    _quit = False


    def __init__(self, title):
        self.title = title
        self._containers = []
        self._containers_right = []
        self._containers_bottom = []
        App.window = self
        self.default_size = 200
        self.dirty = 1
        self._containers_width = 0
        self._containers_height = 0
        self.repaint_areas = []
        self.window_surface = None
        self.log_events = "None"
        self._exit_code = 0
        self.event_console = None
        self.action_bar = None
        self.event_queue = deque()
        self.docks = 0
        self.actor_toolbar = None
        self.level_designer = None
        self.full_screen = False
        self.color_console = False
        self.dirty = True
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, "../resources/logo_small_32.png")
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except:
            pass

    def _display_update(self):
        self._recalculate_dimensions()
        if self.full_screen:
            #self.window_surface = pygame.display.set_mode((self.window_width, self.window_height),
            #                                              pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height, ), pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.window_surface.set_alpha(None)

    def run(self, image, full_screen: bool = False, log=False):
        """
        runs the main_loop

        Lines after this statement are not reachable

        Args:
            self:
            image:
            full_screen:
            log:

        Returns:

        """
        self.full_screen = full_screen
        self._recalculate_dimensions()
        self._setup_images()
        self._display_update()
        pygame.display.update([image.get_rect()])
        if log is True:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.window.window_surface.blit(image, self.board.rect)
        App.log.info(
            "Created window with width: {0}, height: {1}".format(self.window_width, self.window_height))
        # Start the main-loop
        print("run")
        while not App._quit:
            self._update()
        pygame.display.quit()
        sys.exit(self._exit_code)

    def _setup_images(self):
        from pathlib import Path
        from miniworldmaker.appearances import appearance
        jpgs = list(Path("./images/").rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path("./images/w wwsdsdwasd").rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path("./images/").rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            _image = appearance.Appearance.load_image(img_path)

    def _update(self):
        self._process_pygame_events()
        if self.dirty:
            self._display_update()
            self.dirty = False
        if not App._quit:
            self.repaint_areas = []
            if self.dirty:
                self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
                self.dirty = 0
            # Event handling
            while self.event_queue:
                element = self.event_queue.pop()
                for ct in self._containers:
                    ct.handle_event(element[0], element[1])
            self.event_queue.clear()
            # self.board.collision_handling
            for ct in self._containers:
                if ct.dirty:
                    ct.update()
                    ct.repaint()
                    ct.blit_surface_to_window_surface()
            pygame.display.update(self.repaint_areas)
            self.repaint_areas = []


    def _update_containers(self):
        top_left = 0
        for ct in self._containers_right:
            ct.container_top_left_x = top_left
            top_left += ct.container_width
        top_left = 0
        for ct in self._containers_bottom:
            ct.container_top_left_y = top_left
            top_left += ct.container_height
        self.dirty = 1

    def add_container(self, container, dock, size=None) -> container_file.Container:
        self._recalculate_dimensions()
        for ct in self._containers:
            print("add container", container, self.window_height)
        if dock == "right" or dock == "top_left":
            self._containers_right.append(container)
        if dock == "bottom" or dock == "top_left":
            self._containers_bottom.append(container)
        self._containers.append(container)
        if size is None:
            size = container.default_size
        container._add_to_window(self, dock, size)
        self._display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1
        if self.board:
            for token in self.board.tokens:
                token.dirty = 1
        return container

    def remove_container(self, container):
        self._containers.remove(container)
        if container in self._containers_right:
            self._containers_right.remove(container)
        if container in self._containers_bottom:
            self._containers_bottom.remove(container)
        #self._display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1
        if self.board:
            for token in self.board._tokens:
                token.dirty = 1
        self._update_containers()
        self._update()

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self._containers:
            container.remove()
            self.remove_container(container)

    def _recalculate_dimensions(self):
        self._update_containers()
        containers_width = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_width = container.container_width
            elif container.window_docking_position == "right":
                containers_width += container.container_width
            elif container.window_docking_position == "main":
                containers_width = container.container_width
        containers_height = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_height = container.container_height
            elif container.window_docking_position == "bottom":
                containers_height += container.container_height
            elif container.window_docking_position == "main":
                containers_height = container.container_height
        self.dirty = 1
        self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
        self._containers_width, self._containers_height = containers_width, containers_height

    @property
    def window_width(self):
        return self._containers_width

    @property
    def window_height(self):
        return self._containers_height

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self._containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container
        return None

    def _process_pygame_events(self):
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
            if "STRG" in key_codes and "Q" in key_codes:
                self.quit()
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
            self.key_pressed(keys.key_codes_to_keys(keys_pressed))
        for event in pygame.event.get():
            # Event: Quit
            if event.type == pygame.QUIT:
                self.quit()
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.send_mouse_down(event)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.send_event_to_containers("mouse_motion", (pos[0], pos[1]))
                # key-events
            elif event.type == pygame.KEYUP:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                self.send_event_to_containers("key_up", keys_pressed)
            elif event.type == pygame.KEYDOWN:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                if "F5" in keys_pressed:
                    if not self.event_console:
                        self.event_console = event_console.EventConsole()
                        self.add_container(self.event_console, dock="right")
                        if self.docks == 0:
                            self.action_bar = a_bar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.log.info("Added event console")
                    elif self.event_console:
                        self.remove_container(self.event_console)
                        self.docks -= 1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                            self.running = True
                        self.event_console = None
                elif "F6" in keys_pressed:
                    if not self.actor_toolbar:
                        self.actor_toolbar = inspect_actor_toolbar.InspectActorToolbar(self.board)
                        if self.docks == 0:
                            self.action_bar = a_bar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.actor_toolbar, dock="right")
                        self.log.info("Added active actor toolbar")
                    elif self.actor_toolbar:
                        self.remove_container(self.actor_toolbar)
                        self.docks -= 1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                            self.board.is_running = True
                        self.actor_toolbar = None
                elif "F7" in keys_pressed:
                    if not self.level_designer:
                        self.level_designer = level_designer_toolbar.LevelDesignerToolbar(self.board)
                        if self.docks == 0:
                            self.action_bar = a_bar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.level_designer, dock="right")
                        self.log.info("Added level designer")
                    elif self.level_designer:
                        self.remove_container(self.level_designer)
                        self.level_designer = None
                        self.docks -= 1
                        if self.docks == 0:
                            self.board.is_running = True
                            self.remove_container(self.action_bar)
                elif "F8" in keys_pressed:
                    if not self.color_console:
                        self.color_console = color_toolbar.ColorToolbar(self.board)
                        if self.docks == 0:
                            self.action_bar = a_bar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.color_console, dock="right")
                        self.log.info("Added level designer")
                    elif self.color_console:
                        self.remove_container(self.color_console)
                        self.color_console = None
                        self.docks -= 1
                        if self.docks == 0:
                            self.board.is_running = True
                            self.remove_container(self.action_bar)
                else:
                    self.send_event_to_containers("key_down", keys_pressed)
        return False

    def send_mouse_down(self, event):
        pos = pygame.mouse.get_pos()
        #container_set = set()
        #clicked_container = self.get_container_by_pixel(pos[0], pos[1])
        #container_set.add(clicked_container)  # add container which was clicked
        #for container in container_set:
        if event.button == 1:
            self.send_event_to_containers("mouse_left", (pos[0], pos[1]))
        if event.button == 3:
            self.send_event_to_containers("mouse_right", (pos[0], pos[1]))
        if event.button == 4:
            self.send_event_to_containers("wheel_up", (pos[0], pos[1]))
        if event.button == 5:
            self.send_event_to_containers("wheel_down", (pos[0], pos[1]))
        for token in self.board.tokens:
            if hasattr(token, "on_clicked_left"):
                if token.sensing_point(pos):
                    self.send_event_to_containers("clicked_left", (token, (pos[0], pos[1])))

    def send_event_to_containers(self, event, data):
        events = []
        for container in self._containers:
            e = event, data
            if (event in container.registered_events or "all" in container.registered_events) and event not in events:
                self.event_queue.appendleft(e)
                events.append(event)

    def get_keys(self):
        key_codes = [key]
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes

    def quit(self, exit_code = 0):
        self._exit_code = exit_code
        App._quit = True

    def key_pressed(self, key):
        def wrapper_accepting_arguments(key):
            function(key)

        return wrapper_accepting_arguments
