from typing import Tuple
import pygame

from miniworldmaker.board_positions import board_position
import miniworldmaker
from miniworldmaker.exceptions.miniworldmaker_exception import (
    EllipseWrongArgumentsError,
    LineFirstArgumentError,
    LineSecondArgumentError,
    RectFirstArgumentError,
    RectSecondArgumentError,
    RectThirdArgumentError,
)


class Shape(miniworldmaker.Token):
    """Base class for Shapes"""

    def __init__(self, position: tuple = None):
        if position == None:
            position = (0, 0)
        super().__init__(position)
        self.add_costume((100, 0, 0, 0))
        self.costumes.add(self.costume)
        self._color = (255, 255, 255, 255)
        self.costume.is_upscaled = False

    @staticmethod
    def bounding_box(points: Tuple) -> pygame.Rect:
        x_coordinates, y_coordinates = zip(*points)
        x = min(x_coordinates)
        y = min(y_coordinates)
        width = max(x_coordinates) - x
        height = max(y_coordinates) - y
        return pygame.Rect(x, y, width, height)

    @classmethod
    def from_center(cls, position: tuple, color: tuple):
        shape = Shape(position=position, color=color)
        shape.center = position
        return shape

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update()

    def update(self):
        self.costume.draw_shape_set(*self.draw_shape)


class Point(Shape):
    """A Point-Shape

    Args:
        position: The position as 2-tuple
        thickness: The thickness of the point (1: pixel, >1: The point is rendered as circle)

    Examples:
        Creates a red point at position (200,100):

        >>> Point((200, 100), 1)

    """

    def __init__(self, position=(0, 0), thickness: int = 1):
        try:
            super().__init__(rect.topleft)
            rect = pygame.Rect(0, 0, thickness, thickness)
            rect.center = (position[0], position[1])
            self.radius = thickness
            self.thickness = thickness
            self.size = (thickness, thickness)
            self.costume.draw_shape_append(
                pygame.draw.circle,
                [self.color, (int(self.radius), int(self.radius)), int(self.radius), self.thickness],
            )
            self.costume.load_surface()
        except TypeError:
            print("Shape not created because mouse position not in screen")
            self.remove()


class Circle(Shape):
    """
    A Circle-Shape.

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        radius: The radius of the circle
        thickness: The thickness of the bounding line (0: The object is filled)

    Examples:
        Example Creation of a circle

        >>> Circle((200, 100), 20, 1)
        Creates a red circle at position (200,100) with radius 20

        Example Creation of a filled circle

        >>> Circle((200, 100), 20, 0)
        Creates a red circle at position (200,100) with radius 20. The circle is filled
    """

    def __init__(self, position=(0, 0), radius: int = 10, thickness: int = 1):
        super().__init__(position)
        self._thickness = thickness
        self.size = (radius * 2, radius * 2)
        self.costume.draw_shape_set(*self.draw_shape)
        rect = pygame.Rect(0, 0, radius, radius)
        rect.center = (self.position[0], self.position[1])
        self.position = rect.center
        self.center = position

    @property
    def draw_shape(self):
        return pygame.draw.circle, [self.color, (int(self.radius), int(self.radius)), int(self.radius), self.thickness]

    @property
    def radius(self):
        """
        Gets the radius of the circle.
        If you change the circle-size (e.g. with self.size = (x, y), the radius value will be changed too.

        Returns: The radius

        """
        return self.width / 2

    def set_physics_default_values(self):
        self.physics.shape_type = "circle"
        self.physics.can_move = True
        self.physics.stable = False

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self.costume.draw_shape_set(*self.draw_shape)


class Ellipse(Shape):
    def __init__(
        self,
        position=(0, 0),
        width: int = 10,
        height: int = 10,
        thickness: int = 1,
    ):
        self.check_arguments(position, width, height, thickness)
        super().__init__(position)
        self._thickness = thickness
        self._width, self._height = width, height
        self.size = (width, height)
        self.costume.draw_shape_set(*self.draw_shape)
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (self.position[0], self.position[1])
        self.position = rect.center

    def check_arguments(self, position, width, height, thickness):
        if type(position) not in [tuple, None] or type(width) != int or type(height) != int or type(thickness) != int:
            raise EllipseWrongArgumentsError()

    @property
    def draw_shape(self):
        return pygame.draw.ellipse, [
            self.color,
            pygame.Rect((0, 0), (int(self.size[0]), int(self.size[1]))),
            self.thickness,
        ]

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self.costume.draw_shape_set(*self.draw_shape)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.size = (self._width, self._height)
        self.update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.size = (self._width, self._height)
        self.update()


class Line(Shape):
    """A Line-Shape.
    
    Args:

        start_position: The start_position as 2-tuple.
        end_position: The end_position as 2-tuple.
        thickness: The thickness of the bounding line
    

    Examples:

        Example Creation of a line
        >>> Line((200, 100), (400,100), 1)
        Creates a line from (200, 100) to (400, 100)
    """

    def __init__(self, start_position: tuple, end_position: tuple, thickness: int = 1):
        self.check_arguments(start_position, end_position, thickness)
        self._start_position = start_position
        self._end_position = end_position
        self.thickness = thickness
        super().__init__(start_position)
        box = self.get_bounding_box()
        width, height = box[2], box[3]
        self.size = (width, height)
        self.position = start_position
        self.update()

    def check_arguments(self, start_position, end_position, thickness):
        if type(start_position) != tuple:
            raise LineFirstArgumentError(start_position)
        if type(end_position) != tuple:
            raise LineSecondArgumentError(end_position)

    def set_physics_default_values(self):
        self.physics.shape_type = "line"
        self.physics.simulation = "static"

    def get_bounding_box(self):
        width = abs(self.start_position[0] - self.end_position[0]) + 2 * self.thickness
        height = abs(self.start_position[1] - self.end_position[1]) + 2 * self.thickness
        box = pygame.Rect(
            min(self.start_position[0], self.end_position[0]) - self.thickness,
            min(self.start_position[1], self.end_position[1]) - self.thickness,
            width,
            height,
        )
        return box

    def update(self):
        box = self.get_bounding_box()
        # mod_start: Start of line
        _x_start = self.start_position[0] - box.topleft[0]
        _y_start = self.start_position[1] - box.topleft[1]
        self.local_start_position = (_x_start, _y_start)
        # mod end: End of line
        _x_end = self.end_position[0] - box.topleft[0]
        _y_end = self.end_position[1] - box.topleft[1]
        self.local_end_position = (_x_end, _y_end)
        self.costume.draw_shape_set(*self.draw_shape)
        # self.costume.load_surface()
        self.position = self.start_position
        self.costume.dirty = 1

    @property
    def draw_shape(self):
        return pygame.draw.line, [self.color, self.local_start_position, self.local_end_position, self.thickness]

    @property
    def start_position(self):
        return self._start_position

    @start_position.setter
    def start_position(self, value: int):
        self._start_position = value
        self.update()

    @property
    def end_position(self):
        return self._end_position

    @end_position.setter
    def end_position(self, value: int):
        self._end_position = value


class Rectangle(Shape):
    """
    A Rect-Shape.

    Args:
        topleft: Topleft Position of Rect
        height: The height of the rect
        width: The width of the rect
        thickness: The thickness of the bounding line

    Examples:
        Example Creation of a polygon

        >>> Rectangle((200, 100), 10, 10, 1)
        Creates a red rect with the topleft position (200, 100), the height 10 and the width 10
    """

    def __init__(
        self,
        topleft=(0, 0),
        width: int = 10,
        height: int = 10,
        thickness: int = 1,
    ):
        self.check_arguments(topleft, width, height, thickness)
        super().__init__(topleft)
        self.thickness = thickness
        self._width, self._height = (width, height)
        self.size = (self._width, self._height)
        self.update()

    def check_arguments(self, topleft, width, height, thickness):
        if type(topleft) != tuple and type(topleft) != board_position.BoardPosition:
            raise RectFirstArgumentError(topleft)
        if type(width) != int:
            raise RectSecondArgumentError(width)
        if type(height) != int:
            raise RectThirdArgumentError(height)

    def update(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.position[0], self.position[1])
        self.costume.draw_shape_set(*self.draw_shape)

    @property
    def draw_shape(self):
        return pygame.draw.rect, [
            self.color,
            pygame.Rect((0, 0), (int(self.size[0]), int(self.size[1]))),
            self.thickness,
        ]

    def set_physics_default_values(self):
        self.physics.shape_type = "rect"
        self.physics.stable = False
        self.physics.correct_angle = 90

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.size = (self._width, self._height)
        self.update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.size = (self._width, self._height)
        self.update()


class Polygon(Shape):
    """
    A Polygon-Shape.

    Args:
        point-list: A list of points
        thickness: The thickness of the bounding line

    Examples:
        Example Creation of a polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 1,
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)

        Example Creation of a filled polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 0)
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)
    """

    def __init__(self, pointlist, thickness=1):

        super().__init__((0, 0))
        self.thickness = thickness
        self._pointlist = pointlist

    def update(self):
        min_x = min([p[0] for p in self.pointlist])
        min_y = min([p[1] for p in self.pointlist])
        width = max([p[0] - min_x for p in self.pointlist]) + self.thickness
        height = max([p[1] - min_y for p in self.pointlist]) + self.thickness
        self.size = (width, height)
        self.mod_pointlist = []
        for point in self.pointlist:
            x = point[0] - min_x
            y = point[1] - min_y
            self.mod_pointlist.append((x, y))
        self.costume.draw_shape_set(*self.draw_shape)
        self.position = min_x, min_y

    @property
    def draw_shape(self):
        return pygame.draw.polygon, [
            self.color,
            self.mod_pointlist,
            self.thickness,
        ]

    @property
    def pointlist(self):
        return self._pointlist

    @pointlist.setter
    def pointlist(self, value: int):
        self._pointlist = value
        self.update()
