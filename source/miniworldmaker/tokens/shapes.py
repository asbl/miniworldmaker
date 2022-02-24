from typing import Tuple
import pygame
import math
import pygame.gfxdraw
import math

from miniworldmaker.board_positions import board_position
import miniworldmaker
from miniworldmaker.exceptions.miniworldmaker_exception import (
    EllipseWrongArgumentsError,
    LineFirstArgumentError,
    LineSecondArgumentError,
    RectFirstArgumentError,
)


class Shape(miniworldmaker.Token):
    """Shape is the parent class for various geometric objects that can be created.

    Each geometric object has the following properties:

    * border: The border thickness of the object.
    * fill: True/False if the object should be filled.
    * fill_color: The fill color of the object
    * border_color: The border color of the object.

    .. image:: ../_images/shapes.png
        :width: 60%
        :alt: Shapes
    """

    def __init__(self, position: tuple = None):
        if position == None:
            position = (0, 0)
        super().__init__(position)
        self.add_costume((100, 0, 0, 0))
        self.costume.is_upscaled = False
        self._fill = True
        self._border = 1
        self._inner = 0

    def _update_draw_shape(self):
        super()._update_draw_shape()


class Circle(Shape):
    """
    A circular shape, definied by position and radius


    .. image:: ../_images/circle.png
        :width: 120px
        :alt: Circle

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        radius: The radius of the circle


    Examples:
        Create a circle at center position (200,100) with radius 20:

        .. code-block:: python

            Circle((200, 100), 20)

        Create a circle at topleft position

        .. code-block:: python

            miniworldmaker.Circle.from_topleft((100,100),50)
    """

    def __init__(self, position=(0, 0), radius: float = 10):
        self._radius = radius
        self._border = 1
        super().__init__(position)
        self.size = (radius * 2, radius * 2)
        self.center = position

    def _inner_shape(self):
        return pygame.draw.circle, [(self.size[0] / 2, self.size[0] / 2), self.radius, 0]

    def _outer_shape(self):
        return pygame.draw.circle, [(self.size[0] / 2, self.size[0] / 2), self.radius, self.border]

    @classmethod
    def from_topleft(cls, position: tuple, radius: int):
        """Creates a circle with topleft at position"""
        circle = cls(position, radius)
        circle.topleft = circle.center[0], circle.center[1]
        return circle

    @classmethod
    def from_center(cls, position: tuple, radius: float):
        """Creates a circle with center at position"""
        circle = cls(position, radius)
        return circle

    @property
    def radius(self):
        """The radius of the circle.
        If you change the circle-size (e.g. with self.size = (x, y), the radius value will be changed too.
        """
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._update_draw_shape()

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
    """A point is a Circle with Radius 1"""

    def __init__(self, position: tuple):
        """Init a Point at specified position"""
        super().__init__(position, 1)


class Ellipse(Shape):
    """An elliptic shape.

    .. image:: ../_images/ellipse.png
        :width: 120px
        :alt: Ellipse

    Args:
        position: The position as 2-tuple. The ellipse is created at topleft position
        width: The width of the ellipse
        height: The height of the ellipse

    Examples:

        Create an ellipse at topleft position (200,100) with width 20 and height 30

        .. code-block:: python

            Ellipse((200, 100), 20, 30)

        Create an ellipse at center-position (200,100) width width 10 and height 10

        .. code-block:: python

            miniworldmaker.Ellipse.from_center((100,100),10, 10)

        (Alternative) Create an ellipse at center-position (200,100) with width 10 and height 10

        .. code-block:: python

            e = miniworldmaker.Ellipse((100,100),10, 10)
            e.center = e.position
    """

    def __init__(
        self,
        position=(0, 0),
        width: float = 10,
        height: float = 10,
    ):
        self.check_arguments(position, width, height)
        super().__init__(position)
        self._border = 1
        self.size = (width, height)
        self._update_draw_shape()

    def check_arguments(self, position, width, height):
        if type(position) not in [tuple, board_position.BoardPosition, None]:
            raise EllipseWrongArgumentsError()

    def _inner_shape(self):
        return pygame.draw.ellipse, [pygame.Rect(0, 0, self.size[0], self.size[1]), 0]

    def _outer_shape(self):
        return pygame.draw.ellipse, [pygame.Rect(0, 0, self.size[0], self.size[1]), self.border]

    def _update_draw_shape(self):
        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        rect.center = (self.position[0], self.position[1])
        super()._update_draw_shape()

    @classmethod
    def from_topleft(cls, position: tuple, width: float, height: float):
        """Creates an ellipse with topleft at position"""
        ellipse = cls(position, width, height)
        return ellipse

    @classmethod
    def from_center(cls, position: tuple, width: float, height: float):
        """Creates an ellipse with center at position"""
        ellipse = cls(position, width, height)
        ellipse.center = ellipse.position
        return ellipse


class Arc(Ellipse):
    """
    An elliptic Arc.

    Args:
        position: The position as 2-tuple. The ellipse is created at topleft position
        width: The width of the ellipse
        height: The height of the ellipse
        start_angle: The start_angle 
        end_angle: end_angle 

    """
    def __init__(
        self, position=(0, 0), width: float = 10, height: float = 10, start_angle: float = 0, end_angle: float = 0
    ):
        self._start_angle = start_angle
        self._end_angle = end_angle
        if start_angle == end_angle:
            self._end_angle = start_angle + 360
        super().__init__(position, width, height)

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = value
        self._update_draw_shape()

    @property
    def end_angle(self):
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value):
        self._end_angle = value
        self._update_draw_shape()

    def _inner_shape(self):
        p = []
        for n in range(int(self.start_angle), int(self.end_angle), 1):
            x = int(self.size[0] / 2 + self.width / 2 * math.cos(n * math.pi / 180))
            y = int(self.size[1] / 2 - self.height / 2 * math.sin(n * math.pi / 180))
            p.append((x, y))
        p.append((self.size[0] / 2, self.size[1] / 2))
        return pygame.draw.polygon, [p, 0]

    def _outer_shape(self):
        return pygame.draw.arc, [
            pygame.Rect(0, 0, self.size[0], self.size[1]),
            math.radians(self.start_angle),
            math.radians(self.end_angle),
            1,
        ]

    @classmethod
    def from_topleft(cls, position: tuple, width: float, height: float, start_angle, end_angle):
        """Creates a rectangle with topleft at position"""
        rectangle = cls(position, width, height, start_angle, end_angle).center
        return rectangle

    @classmethod
    def from_center(cls, position: tuple, width: float, height: float, start_angle, end_angle):
        """Creates a rectangle with center at position"""
        rectangle = cls(position, width, height, start_angle, end_angle)
        rectangle.center = rectangle.position
        return rectangle


class Line(Shape):
    """A Line-Shape defined by start_position and end_position.

    .. image:: ../_images/ellipse.png
        :width: 120px
        :alt: Line

    Args:

        start_position: The start_position as 2-tuple.
        end_position: The end_position as 2-tuple.

    Examples:

        Create a line from (200, 100) to (400, 100)

        .. code-block:: python

            Line((200, 100), (400,100))

        Create a line from (200, 100) to (400, 100)

        .. code-block:: python

            l = Line((200, 100), (400,100))
            l.border = 2

    """

    def __init__(self, start_position: tuple, end_position: tuple):
        if not start_position or not end_position:
            start_position = (0, 0)
            end_position = (0, 0)
        self.check_arguments(start_position, end_position)
        self._start_position = start_position
        self._end_position = end_position
        super().__init__(start_position)
        self._border = 1
        self._fill = True
        self.position = start_position
        self._update_draw_shape()
        box = self.get_bounding_box()
        self.position = box.topleft

    def check_arguments(self, start_position, end_position):
        if type(start_position) not in [tuple, board_position.BoardPosition, None]:
            raise LineFirstArgumentError(start_position)
        if type(end_position) not in [tuple, board_position.BoardPosition, None]:
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
        width, height = box[2], box[3]
        self.size = (width, height)
        # mod_start: Start of line
        _x_start = self.start_position[0] - box.topleft[0] - self.border
        _y_start = self.start_position[1] - box.topleft[1] - self.border
        self.local_start_position = (_x_start, _y_start)
        # mod end: End of line
        _x_end = self.end_position[0] - box.topleft[0] - self.border
        _y_end = self.end_position[1] - box.topleft[1] - self.border
        self.local_end_position = (_x_end, _y_end)
        super()._update_draw_shape()
        # self.costume.load_surface()

    def _inner_shape(self):
        return pygame.draw.line, [self.local_start_position, self.local_end_position, 0]

    def _outer_shape(self):
        return pygame.draw.line, [self.local_start_position, self.local_end_position, self.border]

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

    @property
    def thickness(self):
        """-> see border"""
        return self.border

    @thickness.setter
    def thickness(self, value):
        self.border = value


class Rectangle(Shape):
    """
    A rectangular shape defined by position, width and height

    .. image:: ../_images/ellipse.png
        :width: 120px
        :alt: Line

    Args:
        topleft: Topleft Position of Rect
        height: The height of the rect
        width: The width of the rect

    Examples:

        Create a rect with the topleft position (200, 100), the width 20 and the height 10

        .. code-block:: python

            Rectangle((200, 100), 20, 10)

    """

    def __init__(
        self,
        topleft=(0, 0),
        width: float = 10,
        height: float = 10,
    ):
        self.check_arguments(topleft, width, height)
        super().__init__(topleft)
        self._border = 1
        self.size = (width, height)
        self._update_draw_shape()

    def check_arguments(self, topleft, width, height):
        if type(topleft) != tuple and type(topleft) != board_position.BoardPosition:
            raise RectFirstArgumentError(topleft)

    def _update_draw_shape(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.position[0], self.position[1])
        super()._update_draw_shape()

    def _inner_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.size[0], self.size[1]), 0]

    def _outer_shape(self):
        return pygame.draw.rect, [pygame.Rect(0, 0, self.size[0], self.size[1]), self.border]

    def set_physics_default_values(self):
        self.physics.shape_type = "rect"
        self.physics.stable = False
        self.physics.correct_angle = 90

    @classmethod
    def from_topleft(cls, position: tuple, width: float, height: float):
        """Creates a rectangle with topleft at position"""
        rectangle = cls(position, width, height).center
        return rectangle

    @classmethod
    def from_center(cls, position: tuple, width: float, height: float):
        """Creates a rectangle with center at position"""
        rectangle = cls(position, width, height)
        rectangle.center = rectangle.position
        return rectangle


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
        return pygame.draw.polygon, [self.mod_pointlist, 0]

    def _outer_shape(self):
        return pygame.draw.polygon, [self.mod_pointlist, self.border]

    @property
    def pointlist(self):
        return self._pointlist

    @pointlist.setter
    def pointlist(self, value: int):
        self._pointlist = value
        self.costume_manager.reload_costume()


class Triangle(Polygon):
    def __init__(self, p1: Tuple, p2: Tuple, p3: Tuple):
        self._border = 1
        pointlist = [p1, p2, p3]
        super().__init__(pointlist)
