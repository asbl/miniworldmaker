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
        self.costume.is_upscaled = False
        self._fill = True
        self._border = 1

    def _update_draw_shape(self):
        super()._update_draw_shape()

class Circle(Shape):
    """
    A circular shape.

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        radius: The radius of the circle

    Examples:
        Example Creation of a circle

        >>> Circle((200, 100), 20)
        Creates a red circle at position (200,100) with radius 20.
    """

    def __init__(self, position=(0, 0), radius: int = 10):
        self._radius = radius
        self._border = 1
        super().__init__(position)
        self.center = position

    def _inner_shape(self):
        return pygame.draw.circle, [(int(self.radius), int(self.radius)), int(self.radius)]

    @property
    def radius(self):
        """The radius of the circle.
        If you change the circle-size (e.g. with self.size = (x, y), the radius value will be changed too.
        """
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.update_shape()

    def set_physics_default_values(self):
        self.physics.shape_type = "circle"
        self.physics.can_move = True
        self.physics.stable = False

    def _update_draw_shape(self):
        self.size = (self.radius * 2, self.radius * 2)
        rect = pygame.Rect(0, 0, self.radius, self.radius)
        rect.center = (self.position[0], self.position[1])
        super()._update_draw_shape()


class Point(Circle):
    """A Point.

    A point is a circle with radius 1.
    """

    def __init__(self, position):
        super().__init__(position, 1)


class Ellipse(Shape):
    """An elliptic shape.

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        width: The width of the ellipse
        height: The height of the ellipse

    Examples:
        Example Creation of a circle

        >>> Circle((200, 100), 20, 30)
        Creates a red circle at position (200,100) with width 20 and height 30
    """

    def __init__(
        self,
        position=(0, 0),
        width: int = 10,
        height: int = 10,
    ):
        self.check_arguments(position, width, height)
        super().__init__(position)
        self._border = 1
        self.size = (width, height)
        self._update_draw_shape()

    def check_arguments(self, position, width, height):
        if type(position) not in [tuple, None] or type(width) != int or type(height) != int:
            raise EllipseWrongArgumentsError()

    def _inner_shape(self):
        return pygame.draw.ellipse, [
            pygame.Rect(0, 0, int(self.size[0]), int(self.size[1])),
        ]

    def _update_draw_shape(self):
        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        rect.center = (self.position[0], self.position[1])
        super()._update_draw_shape()


class Line(Shape):
    """A Line-Shape.

    Args:

        start_position: The start_position as 2-tuple.
        end_position: The end_position as 2-tuple.

    Examples:

        Example Creation of a line
        >>> Line((200, 100), (400,100))
        Creates a line from (200, 100) to (400, 100)
    """

    def __init__(self, start_position: tuple, end_position: tuple):
        self.check_arguments(start_position, end_position, 1)
        self._start_position = start_position
        self._end_position = end_position
        super().__init__(start_position)
        self._border = 1
        self._fill = True
        box = self.get_bounding_box()
        width, height = box[2], box[3]
        self.size = (width, height)
        self.position = start_position
        self._update_draw_shape()
        self.position = self.start_position

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

    def _update_draw_shape(self):
        box = self.get_bounding_box()
        # mod_start: Start of line
        _x_start = self.start_position[0] - box.topleft[0]
        _y_start = self.start_position[1] - box.topleft[1]
        self.local_start_position = (_x_start, _y_start)
        # mod end: End of line
        _x_end = self.end_position[0] - box.topleft[0]
        _y_end = self.end_position[1] - box.topleft[1]
        self.local_end_position = (_x_end, _y_end)
        super()._update_draw_shape()
        # self.costume.load_surface()
        

    def _inner_shape(self):
        return pygame.draw.line, [self.local_start_position, self.local_end_position]

    @property
    def start_position(self):
        return self._start_position

    @start_position.setter
    def start_position(self, value: int):
        self._start_position = value
        self.costume_manager.reload_costume()

    @property
    def end_position(self):
        return self._end_position

    @end_position.setter
    def end_position(self, value: int):
        self._end_position = value
        self.costume_manager.reload_costume()

class Rectangle(Shape):
    """
    A Rect-Shape.

    Args:
        topleft: Topleft Position of Rect
        height: The height of the rect
        width: The width of the rect

    Examples:
        Example Creation of a polygon

        >>> Rectangle((200, 100), 20, 10)
        Creates a red rect with the topleft position (200, 100), the width 20 and the height 10
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
        self.size = (width, height)
        self._update_draw_shape()

    def check_arguments(self, topleft, width, height):
        if type(topleft) != tuple and type(topleft) != board_position.BoardPosition:
            raise RectFirstArgumentError(topleft)
        if type(width) != int:
            raise RectSecondArgumentError(width)
        if type(height) != int:
            raise RectThirdArgumentError(height)

    def _update_draw_shape(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.position[0], self.position[1])
        super()._update_draw_shape()

    def _inner_shape(self):
        return pygame.draw.rect, [pygame.Rect((0, 0), (int(self.size[0]), int(self.size[1])))]

    def set_physics_default_values(self):
        self.physics.shape_type = "rect"
        self.physics.stable = False
        self.physics.correct_angle = 90


class Polygon(Shape):
    """
    A Polygon-Shape.

    Args:
        point-list: A list of points

    Examples:
        Example Creation of a polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)])
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)

        Example Creation of a filled polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)])
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)
    """

    def __init__(self, pointlist):
        self._border = 1
        self._pointlist = pointlist
        super().__init__((0, 0))

    def _update_draw_shape(self):
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
        super()._update_draw_shape()

    def _inner_shape(self):
        return pygame.draw.polygon, [self.mod_pointlist]

    @property
    def pointlist(self):
        return self._pointlist

    @pointlist.setter
    def pointlist(self, value: int):
        self._pointlist = value
        self.costume_manager.reload_costume()
