import sys

import pkg_resources
import pygame
import __main__

from miniworldmaker.exceptions.miniworldmaker_exception import MiniworldMakerError, NoRunError
from miniworldmaker.app import window
from miniworldmaker.app import event_manager
from miniworldmaker.app import container_manager
from miniworldmaker.app import sound_manager


class App:
    """The class app contains the game itself. It's created the first time you call board.shbow().
    """
    board = None
    _quit: bool = False

    def check_for_run_method(self):
        try:
            with open(__main__.__file__) as f:
                if ".run()" not in f.read():
                    raise NoRunError()
        except AttributeError:
            print("can't check if run() is present (This can happen if you are using jupyter notebooks. Resuming)")

    def _output_start(self):
        print("init miniworldmaker app...")
        version = pkg_resources.require("miniworldmaker")[0].version
        print("Show new miniworldmaker v.{0} Window".format(version))
        print("Let's go")

    def __init__(self, title):
        self._output_start()
        self.check_for_run_method()
        self.container_manager: "container_manager.ContainerManager" = container_manager.ContainerManager(self)
        self.mainloop_started: bool = False
        self.event_manager: "event_manager.EventManager" = event_manager.EventManager(self)
        self.sound_manager: "sound_manager.SoundManager" = sound_manager.SoundManager(self)
        self.window: "window.Window" = window.Window(title, self.container_manager, self.event_manager)
        App.app: App = self
        App.window: "window.Window" = self.window
        self._exit_code: int = 0

    def run(self, image, full_screen: bool = False):
        """
        runs the main_loop

        Lines after this statement are not reachable

        Args:
            image:
            full_screen:
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
