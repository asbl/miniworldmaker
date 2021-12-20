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
    """The class app contains the game itself. It's created the first time you call board.run().

    Raises:
        NoRunError: After running the programm, the source of the main module is checked. 
            If it does not contain a run() method (e.g. board.run()), this error is raised.
    """

    board = None

    def check_for_run_method(self):
        try:
            with open(__main__.__file__) as f:
                if ".run(" not in f.read():
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
        self.container_manager: "container_manager.ContainerManager" = container_manager.ContainerManager(
            self)
        self._quit = False
        self._mainloop_started: bool = False
        self.event_manager: "event_manager.EventManager" = event_manager.EventManager(self)
        self.sound_manager: "sound_manager.SoundManager" = sound_manager.SoundManager(self)
        self.window: "window.Window" = window.Window(
            title, self.container_manager, self.event_manager)
        App.app: App = self
        App.window: "window.Window" = self.window
        self._exit_code: int = 0

    def run(self, image, fullscreen: bool = False, fit_desktop = False):
        """
        runs the main_loop

        Lines after this statement are not reachable

        Args:
            image:
            fullscreen:
        """
        self.image = image
        self.window.fullscreen = fullscreen
        self.window.fit_desktop = fit_desktop
        # Start the main-loop
        self._prepare_mainloop()
        self.reload_window()
        if not self._mainloop_started:
            self.start_mainloop()

    def _prepare_mainloop(self):
        self._setup_images()

    def _setup_images(self):
        from pathlib import Path
        from miniworldmaker.appearances import appearance
        jpgs = list(Path("./images/").rglob("*.[jJ][pP][gG]"))
        jpegs = list(Path("./images/w wwsdsdwasd").rglob("*.[jJ][pP][eE][gG]"))
        pngs = list(Path("./images/").rglob("*.[pP][nN][gG]"))
        images = jpgs + jpegs + pngs
        for img_path in images:
            appearance.Appearance.load_image(img_path)

    def start_mainloop(self):
        self._mainloop_started = True
        while not self._quit:
            self._update()
        pygame.display.quit()
        sys.exit(self._exit_code)

    def reload_window(self):
        self.window.recalculate_dimensions()
        self.window.dirty = 1

    def _update(self):
        """
        This is the mainloop. This function is called until the app quits.
        """
        self.event_manager.process_pygame_events()
        if self.window.dirty:
            self.window.recalculate_dimensions()
            self.window.add_display_to_repaint_areas()
            self.window.display_update()
        if not self._quit:
            self.event_manager.handle_event_queue()
            self.container_manager.reload_containers()
            self.window.display_repaint()

    def quit(self, exit_code=0):
        self._exit_code = exit_code
        self._quit = True
