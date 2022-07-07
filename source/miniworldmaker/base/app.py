import __main__
import os
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
        NoRunError: After running the program, the source of the main module is checked.
            If it does not contain a run() method (e.g. board.run()), this error is raised.
    """

    running_board = None
    path = None
    running_app: "App" = None
    init = False
    window: "window.Window" = None

    @staticmethod
    def reset(unittest=False, file=None):
        App.running_board = None
        App.path = None
        App.running_app = None
        App.init = False  # is pygame.init called?
        if file and unittest:
            App.path = os.path.dirname(file)

    @staticmethod
    def check_for_run_method():
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
        self.init_pygame()
        self._output_start()
        self.check_for_run_method()
        self.container_manager: "container_manager.ContainerManager" = container_manager.ContainerManager(self)
        self._quit = False
        self.image = None
        self._unittest = False
        self._mainloop_started: bool = False
        self.event_manager: "event_manager.EventManager" = event_manager.EventManager(self)
        self.sound_manager: "sound_manager.SoundManager" = sound_manager.SoundManager(self)
        self.window: "window.Window" = window.Window(title, self.container_manager, self.event_manager)
        App.running_app = self
        App.window = self.window
        self._exit_code: int = 0
        if App.path:
            self.path = App.path

    def switch_board(self, new_board):
        old_board = App.running_board
        if new_board != old_board:
            App.running_board = new_board
            self.image = new_board.image
            self.container_manager.switch_container(old_board, new_board)
            self._prepare_mainloop()
            new_board.on_setup()

        # new_board.run(event="board_loaded")

    def run(self, image, fullscreen: bool = False, fit_desktop: bool = False, replit: bool = False):
        """
        runs the main_loop
        Args:
            image: The background image
            fullscreen: True or False
            fit_desktop: True or false
            replit: True or false
        """
        self.image = image
        self.window.fullscreen = fullscreen
        self.window.fit_desktop = fit_desktop
        self.window.replit = replit
        # Start the main-loop
        self.init_app()
        self._prepare_mainloop()
        if not self._mainloop_started:
            self.start_mainloop()
        else:
            self.running_board.dirty = 1
            self.running_board.background.set_dirty("all", 2)

    def init_app(self):
        self.init_pygame()
        image_manager.ImageManager.cache_images_in_image_folder()

    def _prepare_mainloop(self):
        self.window.recalculate_dimensions()
        self.window.display_update()
        self.running_board.dirty = 1
        self.running_board.background.set_dirty("all", 2)

    @staticmethod
    def init_pygame():
        pygame.init()

    def start_mainloop(self):
        self._mainloop_started = True
        while not self._quit:
            self._update()
        if not self._unittest:
            pygame.display.quit()
            sys.exit(self._exit_code)

    def _update(self):
        """
        This is the mainloop. This function is called until the app quits.
        """
        self.event_manager.pygame_events_to_event_queue()
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
