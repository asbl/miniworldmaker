from typing import Tuple, Union

import pygame
import pygame.gfxdraw

import miniworldmaker.tokens.token as token
import miniworldmaker.tokens.token_plugins.shapes.shape_costume as shape_costume
from miniworldmaker.positions import position as board_position
from miniworldmaker.positions import vector as board_vector
from miniworldmaker.exceptions.miniworldmaker_exception import (
    EllipseWrongArgumentsError,
    LineFirstArgumentError,
    LineSecondArgumentError,
    RectFirstArgumentError,
)


class Shape(token.Token):
    """Shape is the parent class for various geometric objects that can be created.

    Each geometric object has the following properties:

    * border: The border thickness of the object.
    * is_filled: True/False if the object should be filled.
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

    def new_costume(self):
        return shape_costume.ShapeCostume(self)


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
        super().__init__(position)
        self.position_manager.set_size((self._radius * 2, self._radius * 2), scale=False)
        self.center = position

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
        _center = self.center
        self.position_manager.set_size((self._radius * 2, self._radius * 2), scale=False)
        self.center = _center
        self.costume.set_dirty("scale", self.costume.RELOAD_ACTUAL_IMAGE)

    def set_physics_default_values(self):
        self.physics.shape_type = "circle"
        self.physics.can_move = True
        self.physics.stable = False

    def new_costume(self):
        return shape_costume.CircleCostume(self)

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
        self.costume = shape_costume.EllipseCostume(self)
        self._border = 1
        self.size = (width, height)

    def check_arguments(self, position, width, height):
        if type(position) not in [tuple, board_position.Position, None]:
            raise EllipseWrongArgumentsError()

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
        self.costume = shape_costume.ArcCostume(self)

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = value
        self.costume.set_dirty("draw_shapes", self.costume.RELOAD_ACTUAL_IMAGE)

    @property
    def end_angle(self):
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value):
        self._end_angle = value
        self.costume.set_dirty("draw_shapes", self.costume.RELOAD_ACTUAL_IMAGE)

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

    def __init__(self, start_position: Union[tuple, "board_position.Position"],
                 end_position: Union[tuple, "board_position.Position"]):
        if not start_position or not end_position:
            start_position = (0, 0)
            end_position = (0, 0)
        if type(start_position) not in [tuple, board_position.Position, None]:
            raise LineFirstArgumentError(start_position)
        if type(end_position) not in [tuple, board_position.Position, None]:
            raise LineSecondArgumentError(end_position)
        self._length = 0
        self._start_position = board_position.Position.create(start_position)
        self._end_position = board_position.Position.create(end_position)
        super().__init__(start_position)
        self.costume = shape_costume.LineCostume(self)
        self._update_size()

    @property
    def start_position(self):
        return self._start_position

    start = start_position

    @start_position.setter
    def start_position(self, value):
        self._start_position = board_position.Position.create(value)
        self._update_size()

    @property
    def end_position(self):
        return self._end_position

    end = end_position

    @end_position.setter
    def end_position(self, value):
        self._end_position = board_position.Position.create(value)
        self._update_size()

    @property
    def direction(self):
        return self.position_manager.get_direction()

    @direction.setter
    def direction(self, value):
        self.position_manager.set_direction(value)
        direction_vector = board_vector.Vector.from_direction(self.direction)
        direction_vector = direction_vector.normalize() * self._length * 0.5
        self._start_position = board_position.Position.create(self.center + direction_vector)
        self._end_position = board_position.Position.create(self.center - direction_vector)

    def set_physics_default_values(self):
        self.physics.shape_type = "line"
        self.physics.simulation = "manual"

    def get_bounding_box(self):
        width = abs(self.start_position[0] - self.end_position[0]) + self.thickness
        height = abs(self.start_position[1] - self.end_position[1]) + self.thickness
        box = pygame.Rect(
            min(self.start_position[0], self.end_position[0]) - int(0.5 * self.thickness),
            min(self.start_position[1], self.end_position[1]) - int(0.5 * self.thickness),
            width,
            height,
        )
        return box

    def _update_size(self):
        self._length = self.start_position.distance_to(self._end_position)
        self.position_manager.set_size((self.thickness, self._length + 2 * self.thickness), scale=False)
        self.position_manager.set_direction(self.start_position.direction_to(self._end_position).value)
        self.center = self.start_position + board_vector.Vector.from_positions(self.start_position,
                                                                               self.end_position) * 0.5
        self.costume.set_dirty("all", 1)

    @property
    def length(self):
        return self._length

    @property
    def thickness(self):
        """-> see border"""
        return self.costume.border

    @thickness.setter
    def thickness(self, value):
        self.costume.border = value
        self._update_size()

    @property
    def border(self):
        """-> see border"""
        return self.costume.border

    @border.setter
    def border(self, value):
        self.costume.border = value
        self._update_size()

    line_width = thickness


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
        self.costume = shape_costume.RectangleCostume(self)
        self.size = (width, height)

    def check_arguments(self, topleft, width, height):
        if type(topleft) != tuple and type(topleft) != board_position.Position:
            raise RectFirstArgumentError(topleft)
        if type(width) not in [int, float]:
            raise TypeError("width of Rectangle should be int or float " + str(type(width)))
        if type(height) not in [int, float]:
            raise TypeError("height of Rectangle should be int or float but is " + str(type(height)))

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
        super().__init__((0, 0))
        self._pointlist = pointlist
        self.costume = shape_costume.PolygonCostume(self, pointlist)

    @property
    def pointlist(self):
        return self._pointlist

    @pointlist.setter
    def pointlist(self, value: int):
        self._pointlist = value


class Triangle(Polygon):
    def __init__(self, p1: Tuple, p2: Tuple, p3: Tuple):
        pointlist = [p1, p2, p3]
        super().__init__(pointlist)
