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
        self._fill_color = self.board.fill_color
        self._border_color = self.board.stroke_color

    @staticmethod
    def bounding_box(points: Tuple) -> pygame.Rect:
        x_coordinates, y_coordinates = zip(*points)
        x = min(x_coordinates)
        y = min(y_coordinates)
        width = max(x_coordinates) - x
        height = max(y_coordinates) - y
        return pygame.Rect(x, y, width, height)


    def inner_shape(self):
        pass

    @property
    def color(self):
        return self._fill_color

    @color.setter
    def color(self, value):
        self._fill_color = value
        self.update_shape()

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = value
        self.update_shape()

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, value):
        self._border_color = value
        self.update_shape()

    def update_shape(self):
        self.costume.draw_shapes = []
        inner_shape = self.inner_shape()[0]
        inner_shape_arguments =  [self.fill_color,] + self.inner_shape()[1] + [0,]
        outer_shape_arguments =  [self.border_color,] + self.inner_shape()[1] + [self.border,]
        self.costume.draw_shape_append(inner_shape, inner_shape_arguments)
        if self.border != 0:
            self.costume.draw_shape_append(inner_shape, outer_shape_arguments)
        
    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, value):
        self._border = value
        self.update_shape()





class Circle(Shape):
    """
    A Circle-Shape.

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        radius: The radius of the circle
        border: The border of the bounding line (0: The object is filled)

    Examples:
        Example Creation of a circle

        >>> Circle((200, 100), 20, 1)
        Creates a red circle at position (200,100) with radius 20

        Example Creation of a filled circle

        >>> Circle((200, 100), 20, 0)
        Creates a red circle at position (200,100) with radius 20. The circle is filled
    """

    def __init__(self, position=(0, 0), radius: int = 10):
        self._radius = radius
        self._border = 1
        super().__init__(position)
        self.center = position
        

    def inner_shape(self):
        return pygame.draw.circle, [(int(self.radius), int(self.radius)), int(self.radius)]

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
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.update_shape()

    def update_shape(self):
        self.size = (self.radius * 2, self.radius * 2)
        rect = pygame.Rect(0, 0, self.radius, self.radius)
        rect.center = (self.position[0], self.position[1])
        super().update_shape()

class Point(Circle):
    def __init__(self, position):
        super().__init__(position, 1)


class Ellipse(Shape):
    def __init__(
        self,
        position=(0, 0),
        width: int = 10,
        height: int = 10,
        border: int = 1,
    ):
        self.check_arguments(position, width, height)
        super().__init__(position)
        self._border = 1
        self._width, self._height = width, height
        self.size = (width, height)

    def check_arguments(self, position, width, height):
        if type(position) not in [tuple, None] or type(width) != int or type(height) != int:
            raise EllipseWrongArgumentsError()

    def inner_shape(self):
        return pygame.draw.ellipse, [
            pygame.Rect(0, 0, int(self.size[0]), int(self.size[1])),
        ]

    def update_shape(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.position[0], self.position[1])
        super().update_shape()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.size = (self._width, self._height)
        self.update_shape()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.size = (self._width, self._height)
        self.update_shape()


class Line(Shape):
    """A Line-Shape.

    Args:

        start_position: The start_position as 2-tuple.
        end_position: The end_position as 2-tuple.
        border: The border of the bounding line


    Examples:

        Example Creation of a line
        >>> Line((200, 100), (400,100), 1)
        Creates a line from (200, 100) to (400, 100)
    """

    def __init__(self, start_position: tuple, end_position: tuple):
        self.check_arguments(start_position, end_position, 1)
        self._start_position = start_position
        self._end_position = end_position
        self._border = 1
        super().__init__(start_position)
        box = self.get_bounding_box()
        width, height = box[2], box[3]
        self.size = (width, height)
        self.position = start_position
        self.update_shape()

    def check_arguments(self, start_position, end_position, border):
        if type(start_position) != tuple:
            raise LineFirstArgumentError(start_position)
        if type(end_position) != tuple:
            raise LineSecondArgumentError(end_position)

    def set_physics_default_values(self):
        self.physics.shape_type = "line"
        self.physics.simulation = "static"

    def get_bounding_box(self):
        width = abs(self.start_position[0] - self.end_position[0]) + 2 * self.border
        height = abs(self.start_position[1] - self.end_position[1]) + 2 * self.border
        box = pygame.Rect(
            min(self.start_position[0], self.end_position[0]) - self.border,
            min(self.start_position[1], self.end_position[1]) - self.border,
            width,
            height,
        )
        return box

    def update_shape(self):
        box = self.get_bounding_box()
        # mod_start: Start of line
        _x_start = self.start_position[0] - box.topleft[0]
        _y_start = self.start_position[1] - box.topleft[1]
        self.local_start_position = (_x_start, _y_start)
        # mod end: End of line
        _x_end = self.end_position[0] - box.topleft[0]
        _y_end = self.end_position[1] - box.topleft[1]
        self.local_end_position = (_x_end, _y_end)
        super().update_shape()
        # self.costume.load_surface()
        self.position = self.start_position

    def inner_shape(self):
        return pygame.draw.line, [self.local_start_position, self.local_end_position]

    @property
    def start_position(self):
        return self._start_position

    @start_position.setter
    def start_position(self, value: int):
        self._start_position = value
        self.update_shape()

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
        border: The border of the bounding line

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
    ):
        self.check_arguments(topleft, width, height)
        super().__init__(topleft)
        self._border = 1
        self._width, self._height = (width, height)
        self.size = (self._width, self._height)
        self.update_shape()

    def check_arguments(self, topleft, width, height):
        if type(topleft) != tuple and type(topleft) != board_position.BoardPosition:
            raise RectFirstArgumentError(topleft)
        if type(width) != int:
            raise RectSecondArgumentError(width)
        if type(height) != int:
            raise RectThirdArgumentError(height)

    def update_shape(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.position[0], self.position[1])
        super().update_shape()

    def inner_shape(self):
        return pygame.draw.rect, [
            pygame.Rect((0, 0), (int(self.size[0]), int(self.size[1])))
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
        self.update_shape()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.size = (self._width, self._height)
        self.update_shape()


class Polygon(Shape):
    """
    A Polygon-Shape.

    Args:
        point-list: A list of points
        border: The border of the bounding line

    Examples:
        Example Creation of a polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 1,
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)

        Example Creation of a filled polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 0)
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)
    """

    def __init__(self, pointlist):
        self._border = 1
        self._pointlist = pointlist
        super().__init__((0, 0))


    def update_shape(self):
        min_x = min([p[0] for p in self.pointlist])
        min_y = min([p[1] for p in self.pointlist])
        width = max([p[0] - min_x for p in self.pointlist]) + self.border
        height = max([p[1] - min_y for p in self.pointlist]) + self.border
        self.size = (width, height)
        self.mod_pointlist = []
        for point in self.pointlist:
            x = point[0] - min_x
            y = point[1] - min_y
            self.mod_pointlist.append((x, y))
        self.position = min_x, min_y
        super().update_shape()

    def inner_shape(self):
        return pygame.draw.polygon, [self.mod_pointlist]
        

    @property
    def pointlist(self):
        return self._pointlist

    @pointlist.setter
    def pointlist(self, value: int):
        self._pointlist = value
        self.update_shape()
