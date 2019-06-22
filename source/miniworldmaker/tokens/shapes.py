import pygame
from miniworldmaker.tokens import token as tk


class Shape(tk.Token):

    def __init__(self, position: tuple, color: tuple):
        super().__init__(position)
        self.costume.fill_color = (200, 0, 0, 0)
        self.color = color


    @staticmethod
    def bounding_box(points):
        x_coordinates, y_coordinates = zip(*points)
        return [min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)]


class Point(Shape):
    """
    A Point-Shape

    Args:
        position: The position as 2-tuple
        thickness: The thickness of the point (1: pixel, >1: The point is rendered as circle)
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a point

        >>> Point((200, 100), 1, color=(255,0,0,255))
        Creates a red point at position (200,100)
    """
    def __init__(self, position, thickness: int = 1, color: tuple = (255, 255, 255, 255)):
        try:
            rect = pygame.Rect(0, 0, thickness, thickness)
            rect.center = (position[0], position[1])
            super().__init__(rect.topleft, color)
            self.size = (thickness, thickness)
            pygame.draw.circle(self.costume.image, self.color, self.costume.image.get_rect().center, thickness, thickness)
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
    def __init__(self, position, radius: int=10, thickness: int= 1, color: tuple = (255, 255, 255, 255)):
        try:
            rect = pygame.Rect(0, 0, radius, radius)
            rect.center = (position[0], position[1])
            super().__init__(rect.topleft, color)
            self.size = (radius*2, radius*2)
            pygame.draw.circle(self.costume.image, self.color, self.costume.image.get_rect().center, radius, thickness)
        except TypeError:
            print("Shape not created because mouse position not in screen")
            self.remove()

    @property
    def radius(self):
        """
        Gets the radius of the circle.
        If you change the circle-size (e.g. with self.size = (x, y), the radius value will be changed too.

        Returns: The radius

        """
        return self.width / 2


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

    def __init__(self, position, width=20, height=20, thickness: int= 1, color: tuple = (255, 255, 255, 255)):
        try:
            rect = pygame.Rect(0, 0, width, height)
            rect.center = (position[0], position[1])
            super().__init__(rect.topleft, color)
            self.size = (width, height)
            pygame.draw.ellipse(self.costume.image, self.color, self.costume.image.get_rect(), thickness)
        except TypeError:
            print("Shape not created because mouse position not in screen")
            self.remove()
        except ValueError:
            print("ERROR: thickness of {0} is greater than ellipse-radius".format(thickness))
            self.remove()

    @property
    def width(self):
        """
        Gets the width of the ellipse
        If you change the ellipse-size (e.g. with self.size = (x, y), the value will be changed too.

        Returns: The width of the ellipse

        """
        return self.width

    @property
    def height(self):
        """
        Gets the height of the ellipse
        If you change the ellipse-size (e.g. with self.size = (x, y), the value will be changed too.

        Returns: The height of the ellipse

        """
        return self.height


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

    def __init__(self, start_position, end_position, thickness=1, color: tuple = (255, 255, 255, 255), ):
        try:
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
        except TypeError:
            print("Shape not created because mouse position not in screen")
            self.remove()


class Polygon(Shape):
    """
    A Polygon-Shape.

    Args:
        point-list: A list of points
        thickness: The thickness of the bounding line
        color: The color as 4-tuple (r, g, b, alpha)

    Examples:
        Example Creation of a polygon

        >>> Line([(200, 100), (400,100), (0, 0)], 1, color=(255,0,0,255))
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)

        Example Creation of a filled polygon

        >>> Line([(200, 100), (400,100), (0, 0)], 0, color=(255,0,0,255))
        Creates a red polygon with the vertices (200, 100) , (400, 100) and (0, 0)
    """

    def __init__(self, pointlist, thickness=1, color: tuple = (255, 255, 255, 255)):
        try:
            box = self.bounding_box(pointlist)
            super().__init__((box[0], box[1]), color)
            self.size = (abs(box[0]-box[2])+4, abs(box[1]-box[3])+4)
            mod_pointlist = []
            for point in pointlist:
                x = point[0]-box[0]
                y = point[1]-box[1]
                mod_pointlist.append((x, y))
            pygame.draw.polygon(self.costume.image, color, mod_pointlist, thickness)
        except TypeError:
            print("Shape not created because mouse position not in screen")
            self.remove()


