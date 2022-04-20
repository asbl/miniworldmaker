import __main__
import sys
import warnings

import pkg_resources
import pygame

import miniworldmaker.appearances.managers.image_manager as image_manager
import miniworldmaker.base.container_manager as container_manager
import miniworldmaker.base.event_manager as event_manager
import miniworldmaker.base.sound_manager as sound_manager
import miniworldmaker.base.window as window


class App:
    """The class app contains the game itself. It's created the first time you call board.run().

    Raises:
        NoRunError: After running the programm, the source of the main module is checked.
            If it does not contain a run() method (e.g. board.run()), this error is raised.
    """

    board = None
    path = None

    def check_for_run_method(self):
        try:
            with open(__main__.__file__) as f:
                if ".run(" not in f.read():
                    warnings.warn(
                        "[boardname].run() was not found in your code. This must be the last line in your code \ne.g.:\nboard.run()\n if your board-object is named board.")
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
        self._quit = False
        self._mainloop_started: bool = False
        self.event_manager: "event_manager.EventManager" = event_manager.EventManager(self)
        self.sound_manager: "sound_manager.SoundManager" = sound_manager.SoundManager(self)
        self.window: "window.Window" = window.Window(title, self.container_manager, self.event_manager)
        App.app: App = self
        App.window: "window.Window" = self.window
        self._exit_code: int = 0

    def run(self, image, fullscreen: bool = False, fit_desktop: bool = False, replit: bool = False):
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
        self.window.replit = replit
        # Start the main-loop
        self._prepare_mainloop()
        if not self._mainloop_started:
            self.start_mainloop()

    def _prepare_mainloop(self):
        self.window.recalculate_dimensions()
        self.window.display_update()
        image_manager.ImageManager.cache_images_in_image_folder()

    def start_mainloop(self):
        self._mainloop_started = True
        self.board.dirty = 1
        self.board.background.dirty = 1
        while not self._quit:
            self._update()
        pygame.display.quit()
        sys.exit(self._exit_code)

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

    def register_path(self, path):
        self.path = path
        App.path = path
