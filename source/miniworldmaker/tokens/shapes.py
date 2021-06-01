import pygame
from miniworldmaker.tokens import token as tk
from miniworldmaker.appearances import costume


class Shape(tk.Token):
    """
    Base class for Shapes
    """

    def __init__(self, position: tuple = None, color: tuple = (255, 255, 255, 255)):
        super().__init__(position)
        self.add_costume((100,0,0,0))
        self.costumes.add(self.costume)
        self.color = color
        self.costume.is_upscaled = False

    @staticmethod
    def bounding_box(points) -> pygame.Rect:
        x_coordinates, y_coordinates = zip(*points)
        x = min(x_coordinates)
        y = min(y_coordinates)
        width = max(x_coordinates) - x
        height = max(y_coordinates) - y
        return pygame.Rect(x, y, width, height)


class Point(Shape):
    """
    A Point-Shape

    Args:
        position: The position as 2-tuple
        thickness: The thickness of the point (1: pixel, >1: The point is rendered as circle)
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Creates a red point at position (200,100):

        >>> Point((200, 100), 1, color=(255,0,0,255))

    """

    def __init__(self, position=None, thickness: int = 1, color: tuple = (255, 255, 255, 255)):
        try:
            rect = pygame.Rect(0, 0, thickness, thickness)
            rect.center = (position[0], position[1])
            self.radius = thickness
            self.thickness = thickness
            super().__init__(rect.topleft, color)
            self.size = (thickness, thickness)
            self.costume.draw_shape_append(pygame.draw.circle, [self.color,
                                                                (int(self.radius), int(self.radius)),
                                                                int(self.radius),
                                                                self.thickness])
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
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a circle

        >>> Circle((200, 100), 20, 1, color=(255,0,0,255))
        Creates a red circle at position (200,100) with radius 20

        Example Creation of a filled circle

        >>> Circle((200, 100), 20, 0, color=(255,0,0,255))
        Creates a red circle at position (200,100) with radius 20. The circle is filled
    """

    def __init__(self, position=None, radius: int = 10, thickness: int = 1, color: tuple = (255, 255, 255, 255)):
        try:

            self._thickness = thickness
            self.color = color
            super().__init__(position, color)
            self.size = (radius * 2, radius * 2)
            self.costume.draw_shape_set(*self.draw_shape)
            rect = pygame.Rect(0, 0, radius, radius)
            rect.center = (self.position[0], self.position[1])
            self.position = rect.center
        except TypeError as e:
            raise e

    @property
    def draw_shape(self):
        return pygame.draw.circle, [self.color,
                                    (int(self.radius), int(self.radius)),
                                    int(self.radius),
                                    self.thickness]

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
    """
    An Ellipse-Shape.

    Args:
        position: The position as 2-tuple. The circle is created with its center at the position
        width: The width of the ellipse
        height: The height of the ellipse
        thickness: The thickness of the bounding line (0: The object is filled)
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of an ellipse

        >>> Circle((200, 100), 20, 40, 1, color=(255,0,0,255))
        Creates an red ellise at position (200,100) with width 20 and height 40

        Example Creation of a filled ellipse

        >>> Circle((200, 100), 20, 40, 0, color=(255,0,0,255))
        Creates a red circle at position (200,100) with width 20 and height 40. The ellipse is filled
    """

    def __init__(self, position=None, width=20, height=20, thickness: int = 1, color: tuple = (255, 255, 255, 255)):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (position[0], position[1])
        self._width = width
        self._height = height
        super().__init__(rect.topleft, color)
        self.size = (width, height)
        self._thickness = thickness

        self.thickness = thickness

    @property
    def draw_shape(self):
        return pygame.draw.ellipse, [self.color,
                                     pygame.Rect(0, 0,
                                                 int(self.width), int(self.height)),
                                     self.thickness]

    @property
    def width(self):
        """
        Gets the width of the ellipse
        If you change the ellipse-size (e.g. with self.size = (x, y), the value will be changed too.

        Returns: The width of the ellipse

        """
        return self._width

    @property
    def height(self):
        """
        Gets the height of the ellipse
        If you change the ellipse-size (e.g. with self.size = (x, y), the value will be changed too.

        Returns: The height of the ellipse

        """
        return self._height

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self.costume.draw_shape_set(*self.draw_shape)


class Line(Shape):
    """
    A Line-Shape.

    Args:
        start_position: The start_position as 2-tuple.
        end_position: The end_position as 2-tuple.
        thickness: The thickness of the bounding line
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a line

        >>> Line((200, 100), (400,100), 1, color=(255,0,0,255))
        Creates a line from (200, 100) to (400, 100)
    """

    def __init__(self,
                 start_position: tuple,
                 end_position: tuple,
                 thickness: int = 1,
                 color: tuple = (255, 255, 255, 255), ):
        try:
            if type(start_position) == int:
                raise TypeError("Error: First argument ist int - Should be tuple or BoardPosition, value",
                                start_position, ", type:", type(start_position))
            if type(end_position) == int:
                raise TypeError("Error: First argument ist int - Should be tuple or BoardPosition, value", end_position,
                                ", type:", type(end_position))
            width = abs(start_position[0]-end_position[0])+ 2 * thickness
            height = abs(start_position[1] - end_position[1]) + 2 * thickness
            box = pygame.Rect(min(start_position[0], end_position[0]) - thickness,
                              min(start_position[1], end_position[1]) - thickness,
                              width,
                              height)
            self.thickness = thickness
            box_width = width
            box_height = height
            # mod_start
            x = start_position[0] - box.topleft[0]
            y = start_position[1] - box.topleft[1]
            self.mod_start = (x, y)
            # mod end
            x = end_position[0] - box.topleft[0]
            y = end_position[1] - box.topleft[1]
            self.mod_end = (x, y)
            self.start_position = start_position
            self.end_position = end_position
            self.local_start_position = self.mod_start
            self.local_end_position = self.mod_end
            super().__init__(box.topleft, color)
            self.size = (box_width, box_height)
            self.costume.draw_shape_append(pygame.draw.line, [self.color,
                                                              self.mod_start,
                                                              self.mod_end,
                                                              self.thickness])
            self.costume.load_surface()

        except TypeError as e:
            raise e

    def set_physics_default_values(self):
        self.physics.shape_type = "line"
        self.physics.gravity = False
        self.physics.can_move = False


class Rectangle(Shape):
    """
    A Rect-Shape.

    Args:
        topleft: Topleft Position of Rect
        height: The height of the rect
        width: The width of the rect
        thickness: The thickness of the bounding line
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a polygon

        >>> Rectangle((200, 100), 10, 10, 1, color=(255,0,0,255))
        Creates a red rect with the topleft position (200, 100), the height 10 and the width 10
    """

    def __init__(self, topleft, width, height, thickness=1, color: tuple = (255, 255, 255, 255)):
        try:
            if type(topleft) != tuple:
                raise TypeError("Error: First argument topleft should be a 2-tuple")
            point_list = []
            self.mod_pointlist = []
            point_list.append(topleft)
            point_list.append((topleft[0] + width, topleft[1]))
            point_list.append((topleft[0] + width, topleft[1] + height))
            point_list.append((topleft[0], topleft[1] + height))
            box = self.bounding_box(point_list)
            self.thickness = thickness
            for point in point_list:
                x = point[0] - box[0]
                y = point[1] - box[1]
                self.mod_pointlist.append((x, y))
            super().__init__((box[0], box[1]), color)
            self.size = (abs(box[2]+self.thickness), abs(box[3]+self.thickness))
            self.costume.draw_shape_set(*self.draw_shape)
            self.physics.correct_angle = 90

        except TypeError as e:
            self.remove()
            raise e

    @property
    def draw_shape(self):
        return pygame.draw.polygon, [self.color,
                                     self.mod_pointlist,
                                     self.thickness,
                                     ]

    def set_physics_default_values(self):
        self.physics.shape_type = "rect"
        self.physics.stable = False


class Polygon(Shape):
    """
    A Polygon-Shape.

    Args:
        point-list: A list of points
        thickness: The thickness of the bounding line
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 1, color=(255,0,0,255))
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)

        Example Creation of a filled polygon

        >>> Polygon([(200, 100), (400,100), (0, 0)], 0, color=(255,0,0,255))
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)
    """

    def __init__(self, pointlist, thickness=1, color: tuple = (255, 255, 255, 255)):
        try:
            box = self.bounding_box(pointlist)
            super().__init__((box[0], box[1]), color)
            self.size = (abs(box[0] - box[2]) + 4, abs(box[1] - box[3]) + 4)
            self.mod_pointlist = []
            self.thickness = thickness
            for point in pointlist:
                x = point[0] - box[0]
                y = point[1] - box[1]
                self.mod_pointlist.append((x, y))
            self.costume.draw_shape_set(*self.draw_shape)
        except TypeError as e:
            raise e

    @property
    def draw_shape(self):
        return pygame.draw.polygon, [self.color,
                                     self.mod_pointlist,
                                     self.thickness,
                                     ]
