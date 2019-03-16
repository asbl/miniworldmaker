import os

import pygame
from gamegridp import container

class Actionbar(container.Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 30
        self.position="bottom"

    def add_to_grid(self, grid):
        super().add_to_grid(grid)

    def _draw_surface(self, surface):
        """
                Draws the action bar
                """
        self.container_surface = self._create_surface()
        surface = self.container_surface
        package_directory = os.path.dirname(os.path.abspath(__file__))
        myfont = pygame.font.SysFont("monospace", 15)
        # Act Button:
        path = os.path.join(package_directory, "data", 'play.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (5, 5))
        label = myfont.render("Act", 1, (0, 0, 0))
        surface.blit(label, (30, 5))
        # Run Button:
        if not self.__grid.is_running:
            path = os.path.join(package_directory, "data", 'run.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            surface.blit(image, (60, 5))
            label = myfont.render("Run", 1, (0, 0, 0))
            surface.blit(label, (85, 5))
        if self.__grid.is_running:
            path = os.path.join(package_directory, "data", 'pause.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (20, 20))
            surface.blit(image, (60, 5))
            label = myfont.render("Pause", 1, (0, 0, 0))
            surface.blit(label, (85, 5))
            # Reset Button:
        path = os.path.join(package_directory, "data", 'reset.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (140, 5))
        label = myfont.render("Reset", 1, (0, 0, 0))
        surface.blit(label, (165, 5))
        # Info-Button
        path = os.path.join(package_directory, "data", 'question.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (225, 5))
        label = myfont.render("Info", 1, (0, 0, 0))
        surface.blit(label, (245, 5))
        # Info-Button
        path = os.path.join(package_directory, "data", 'left.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (285, 5))
        label = myfont.render("Speed:" + str(self.__grid.speed), 1, (0, 0, 0))
        surface.blit(label, (305, 5))
        path = os.path.join(package_directory, "data", 'right.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (380, 5))

    def call_click_event(self, button, pos_x, pos_y):
        self.dirty = 1
        if pos_x > 5 and pos_x < 60:
            # Click on Button Act
            if not self.__grid.is_running:
                self.__grid._act_all()
        elif pos_x > 60 and pos_x < 120:
            # Click on Button Run
            if not self.__grid.is_running:
                self.__grid.run()
            elif self.__grid.is_running:
                self.__grid.stop()
        elif pos_x > 120 and pos_x < 220:
            # Click on Button Reset
            self.__grid.stop()
            self.__grid.reset()
        elif pos_x > 220 and pos_x < 280:
            # Click on Button Info
            if self.__grid.show_info_overlay:
                self.__grid.show_info_overlay = False
            else:
                self.__grid.show_info_overlay = True
        elif pos_x > 285 and pos_x < 345:
            # Click on Button Speed down
            if self.__grid.speed > 0:
                self.__grid.speed = self.__grid.speed - 1
        elif pos_x > 345 and pos_x < 395:
            # Click on Button Speed up
            if self.__grid.speed < 60:
                self.__grid.speed = self.__grid.speed + 1
        return None



