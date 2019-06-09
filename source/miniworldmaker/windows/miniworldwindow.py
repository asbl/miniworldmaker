import logging
import os
import sys

import pkg_resources
import pygame
import miniworldmaker.containers.actionbar as actionbar
from miniworldmaker.containers import inspect_actor_toolbar
from miniworldmaker.containers import container as container_file
from miniworldmaker.containers import event_console
from miniworldmaker.containers import level_designer_toolbar
from miniworldmaker.containers import color_toolbar
from miniworldmaker.tools import keys


class MiniWorldWindow:
    log = logging.getLogger("miniworldmaker")
    board = None
    window = None
    quit = False

    def __init__(self, title):
        self.title = title
        self._containers = []
        self._containers_right = []
        self._containers_bottom = []
        MiniWorldWindow.window = self
        self.default_size = 200
        self.dirty = 1
        self.repaint_areas = []
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.DOUBLEBUF)
        self.window_surface.set_alpha(None)
        self.log_events = "None"
        self.event_console = None
        self.action_bar = None
        self.docks = 0
        self.actor_toolbar = None
        self.level_designer = None
        self.full_screen = False
        self.color_console = False
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, "../resources/logo_small_32.png")
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except:
            pass

    def display_update(self):
        if self.full_screen:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height),
                                                          pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))

    def show(self, image, full_screen : bool = False, log = False):
        self.full_screen = full_screen
        self.display_update()
        if log is True:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.help()
        self.window.window_surface.blit(image, self.board.rect)
        MiniWorldWindow.log.info("Created window with width: {0}, height: {1}".format(self.window_width, self.window_height))
        pygame.display.update([image.get_rect()])
        while not MiniWorldWindow.quit:
            self.update()
            pass
        pygame.quit()

    def update(self):
        self.process_pygame_events()
        if not MiniWorldWindow.quit:
            self.repaint_areas = []
            if self.dirty:
                self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
                self.dirty = 0
            for ct in self._containers:
                ct.update()
                if ct.dirty:
                    ct.repaint()
                    ct.blit_surface_to_window_surface()
            pygame.display.update(self.repaint_areas)
            self.repaint_areas = []

    def update_containers(self):
        top_left = 0
        for ct in self._containers_right:
            ct.container_top_left_x = top_left
            top_left += ct.container_width

        top_left = 0
        for ct in self._containers_bottom:
            ct.container_top_left_y = top_left
            top_left += ct.container_height

    def add_container(self, container, dock, size=None) -> container_file.Container:
        if dock == "right" or dock == "top_left":
            self._containers_right.append(container)
        if dock == "bottom" or dock == "top_left":
            self._containers_bottom.append(container)
        self._containers.append(container)
        if size is None:
            size = container.default_size
        container._add_to_window(self, dock, size)
        self.display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1
        if self.board:
            for token in self.board._tokens:
                token.dirty = 1
        return container

    def remove_container(self, container):
        self._containers.remove(container)
        if container in self._containers_right:
            self._containers_right.remove(container)
        if container in self._containers_bottom:
            self._containers_bottom.remove(container)
        self.display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1
        if self.board:
            for token in self.board._tokens:
                token.dirty = 1
        self.update_containers()
        self.update()

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
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
            if "STRG" in key_codes and "Q" in key_codes:
                self._call_quit_event()
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
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
                        self.send_event_to_containers("mouse_left", (pos[0], pos[1]))
                    if event.button == 3:
                        self.send_event_to_containers("mouse_right", (pos[0], pos[1]))
                    if event.button == 4:
                        self.send_event_to_containers("wheel_up", (pos[0], pos[1]))
                    if event.button == 5:
                        self.send_event_to_containers("wheel_down", (pos[0], pos[1]))
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.send_event_to_containers("mouse_motion", (pos[0], pos[1]))
                # key-events
            elif event.type == pygame.KEYDOWN:
                keys_pressed = keys.key_codes_to_keys(pygame.key.get_pressed())
                if "^" in keys_pressed:
                    tokens_at_pos = self.board.get_tokens_by_pixel(self.board.get_mouse_position())
                    for token in tokens_at_pos:
                        MiniWorldWindow.log.info(token)
                if "F1" in keys_pressed:
                    self.help()
                if "F2" in keys_pressed:
                    if self.log_events is not "all":
                        self.log_events = "all"
                        self.log.info("Log all events")
                    else:
                        self.log_events = "None"
                        self.log.info("Stopped logging events")
                if "F3" in keys_pressed:
                    if self.log_events is not "move":
                        self.log_events = "move"
                        self.log.info("Log move events")
                    else:
                        self.log_events = "None"
                        self.log.info("Stopped logging events")
                if "F4" in keys_pressed:
                    if self.log_events is not "key_events":
                        self.log_events = "key_events"
                        self.log.info("Log key events")
                    else:
                        self.log_events = "None"
                        self.log.info("Stopped logging events")
                if "F5" in keys_pressed:
                    if not self.event_console:
                        self.event_console = event_console.EventConsole()
                        self.add_container(self.event_console, dock="right")
                        if self.docks == 0:
                            self.action_bar = actionbar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks+=1
                        self.log.info("Added event console")
                    elif self.event_console:
                        self.remove_container(self.event_console)
                        self.docks-=1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                        self.event_console = None
                if "F6" in keys_pressed:
                    if not self.actor_toolbar:
                        self.actor_toolbar = inspect_actor_toolbar.InspectActorToolbar()
                        if self.docks == 0:
                            self.action_bar = actionbar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.actor_toolbar, dock="right")
                        self.log.info("Added active actor toolbar")
                    elif self.actor_toolbar:
                        self.remove_container(self.actor_toolbar)
                        self.docks -= 1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                        self.actor_toolbar = None
                if "F7" in keys_pressed:
                    if not self.level_designer:
                        self.level_designer = level_designer_toolbar.LevelDesignerToolbar(self.board)
                        if self.docks == 0:
                            self.action_bar = actionbar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.level_designer, dock="right")
                        self.log.info("Added level designer")
                    elif self.level_designer:
                        self.remove_container(self.level_designer)
                        self.level_designer = None
                        self.docks -= 1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                if "F8" in keys_pressed:
                    if not self.color_console:
                        self.color_console = color_toolbar.ColorToolbar(self.board)
                        if self.docks == 0:
                            self.action_bar = actionbar.ActionBar(self.board)
                            self.add_container(self.action_bar, dock="bottom")
                        self.docks += 1
                        self.add_container(self.color_console, dock="right")
                        self.log.info("Added level designer")
                    elif self.color_console:
                        self.remove_container(self.color_console)
                        self.color_console = None
                        self.docks -= 1
                        if self.docks == 0:
                            self.remove_container(self.action_bar)
                else:
                    self.send_event_to_containers("key_down", keys_pressed)
        return False

    def help(self):
        version = pkg_resources.require("MiniWorldMaker")[0].version
        MiniWorldWindow.log.info("Show new MiniWorldMaker v.{0} Window".format(version))
        MiniWorldWindow.log.info("Press '^' to get Actors at mouse_position")
        MiniWorldWindow.log.info("Press 'F1' to show help")
        MiniWorldWindow.log.info("Press 'F2' to show events in command line")
        MiniWorldWindow.log.info("Press 'F3'  to show move-events in command line")
        MiniWorldWindow.log.info("Press 'F4'  to show key-events in command line")
        MiniWorldWindow.log.info("Press 'F5'  to add Event-console")
        MiniWorldWindow.log.info("Press 'F6'  to add Actor-Toolbar")
        MiniWorldWindow.log.info("Press 'F7'  to add Level-Designer")
        MiniWorldWindow.log.info("Press 'F8'  to add Color-Toolbar")

    def send_event_to_containers(self, event, data):
        for container in self._containers:
            if event in container.register_events or "all" in container.register_events:
                container.pass_event(event, data)
                if "mouse" in event:
                    if "debug" in container.register_events or "mouse" in container.register_events or container == self.get_container_by_pixel(data[0], data[1]):
                        container.get_event(event, data)
                else:
                    container.get_event(event, data)
                if self.log_events == "all":
                    MiniWorldWindow.log.info("Event: '{0}' with data: {1}".format(event, data))
                else:
                    if self.log_events == "move" and event == "move":
                        MiniWorldWindow.log.info("Event: '{0}' with data: {1}".format(event, data))
                    if self.log_events == "key" and (event == "key_pressed" or event == "key_pressed"):
                        MiniWorldWindow.log.info("Event: '{0}' with data: {1}".format(event, data))

    def get_keys(self):
        key_codes = []
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes

    def _call_quit_event(self):
        MiniWorldWindow.quit = True
        pygame.quit()
        sys.exit(0)
