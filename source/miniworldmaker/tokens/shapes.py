from miniworldmaker.tokens import token as tk
from miniworldmaker.boards import board_position as bp
from miniworldmaker.windows import miniworldwindow as wd
import typing
import pygame
import math


class Shape(tk.Token):

    def __init__(self, position: tuple, color: tuple):
        super().__init__(position)
        self.costume.fill_color = (200, 0, 0, 0)
        self.color = color

    @staticmethod
    def bounding_box(points):
        x_coordinates, y_coordinates = zip(*points)
        return [min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)]


class Circle(Shape):

    def __init__(self, position, radius: int=10, thickness: int= 1, color: tuple = (255, 255, 255, 255)):
        rect = pygame.Rect(0, 0, radius, radius)
        rect.center = (position[0], position[1])
        super().__init__(rect.topleft, color)
        self.size = (radius*2, radius*2)
        pygame.draw.circle(self.costume.image, self.color, self.costume.image.get_rect().center, radius, thickness)


class Ellipse(Shape):

    def __init__(self, position, width=20, height=20, thickness: int= 1, color: tuple = (255, 255, 255, 255)):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (position[0], position[1])
        super().__init__(rect.topleft, color)
        self.size = (width, height)
        pygame.draw.ellipse(self.costume.image, self.color, self.costume.image.get_rect(), thickness)


class Point(Shape):

    def __init__(self, position, thickness: int = 1, color: tuple = (255, 255, 255, 255)):
        rect = pygame.Rect(0, 0, thickness, thickness)
        rect.center = (position[0], position[1])
        super().__init__(rect.topleft, color)
        self.size = (thickness, thickness)
        pygame.draw.circle(self.costume.image, self.color, self.costume.image.get_rect().center, thickness, thickness)


class Line(Shape):

    def __init__(self, start_position, end_position, color: tuple = (255, 255, 255, 255), thickness=1):
        box = self.bounding_box([start_position,end_position])
        super().__init__((box[0], box[1]), color)
        # mod_start
        x = start_position[0] - box[0]
        y = start_position[1] - box[1]
        mod_start = (x, y)
        # mod_start
        x = end_position[0] - box[0]
        y = end_position[1] - box[1]
        mod_end = (x, y)
        self.size = (abs(box[0]-box[2])+4, abs(box[1]-box[3])+4)
        pygame.draw.line(self.costume.image, color, mod_start, mod_end, thickness)


class Polygon(Shape):

    def __init__(self, pointlist, color: tuple = (255, 255, 255, 255), thickness=1):
        box = self.bounding_box(pointlist)
        super().__init__((box[0], box[1]), color)
        self.size = (abs(box[0]-box[2])+4, abs(box[1]-box[3])+4)
        mod_pointlist = []
        for point in pointlist:
            x = point[0]-box[0]
            y = point[1]-box[1]
            print(x,y)
            mod_pointlist.append((x, y))
        pygame.draw.polygon(self.costume.image, color, mod_pointlist, thickness)


