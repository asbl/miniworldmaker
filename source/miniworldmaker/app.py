import logging
import traceback
import sys
from collections import deque

import pkg_resources
import pygame
import __main__

import inspect
from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError, NoRunError
from miniworldmaker.window import Window
from miniworldmaker.event_manager import EventManager
from miniworldmaker.container_manager import ContainerManager
from miniworldmaker import sound_manager

version = pkg_resources.require("miniworldmaker")[0].version
print("Show new miniworldmaker v.{0} Window".format(version))
print("Let's go")


class App:
    """The class app contains the game itself. It's created the first time you call board.shbow().
    """
    log = logging.getLogger("miniworldmaker")
    board: "Board" = None
    _quit: bool = False

    def __init__(self, title):
        print("init miniworldmaker app...")
        with open(__main__.__file__) as f:
            if ".run()" not in f.read():
                raise NoRunError()
        self.container_manager: ContainerManager = ContainerManager(self)
        self.mainloop_started = False
        self.event_manager: EventManager = EventManager(self)
        self.sound_manager: sound_manager.SoundManager = sound_manager.SoundManager(self)
        self.window: Window = Window(title, self.container_manager, self.event_manager)
        App.app: App = self
        App.window: Window = self.window
        self._exit_code: int = 0

    def run(self, image, full_screen: bool = False):
        """
        runs the main_loop

        Lines after this statement are not reachable

        Args:
            self:
            image:
            full_screen:
            log:
        """
        self.image = image
        self.full_screen = full_screen
        # Start the main-loop
        self.prepare_mainloop()
        self.reload_window()
        self.mainloop_started = True
        if self.mainloop_started:
            self.start_mainloop()

    def prepare_mainloop(self):
        self._setup_images()

    def start_mainloop(self):
        while not App._quit:
            self._update()
        pygame.display.quit()
        sys.exit(self._exit_code)

    def reload_window(self):
        self.window.recalculate_dimensions()
        self.window.dirty = 1

    def _setup_images(self):
        from pathlib import Path
        from miniworldmaker.appearances import appearance
        jpgs = list(Path("./images/").rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path("./images/w wwsdsdwasd").rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path("./images/").rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            appearance.Appearance.load_image(img_path)

    def _update(self):
        """
        This is the mainloop. This function is called until the app quits.
        """
        self.event_manager.process_pygame_events()
        if self.window.dirty:
            self.window.recalculate_dimensions()
            self.window.reload_repaint_areas()
            self.window.display_update()
        if not App._quit:
            self.event_manager.handle_event_queue()
            
            self.container_manager.reload_containers()
            self.window.display_repaint()
            

    def quit(self, exit_code=0):
        self._exit_code = exit_code
        App._quit = True
