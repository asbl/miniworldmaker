import math
from typing import Union

import numpy as np

import miniworldmaker.positions.direction as board_direction
import miniworldmaker.positions.position as board_position
import miniworldmaker.tokens.token as token_mod


class Vector:
    """Describes a two-dimensional vector.

    It is used to describe a position, acceleration
    or velocity.

    Examples:

        Create a circle which follows the mouse.

        .. code-block:: python

            from miniworldmaker import *
            board = Board(800, 800)

            mover = Circle()
            mover.velocity = Vector(0, 0)
            mover.topspeed = 10


            @board.register
            def act(self):
                mouse_vec = Vector(board.get_mouse_x(), board.get_mouse_y())
                location = Vector.from_token_position(mover)
                acceleration = mouse_vec - location
                acceleration.normalize() * 2

            mover.velocity.add(acceleration)
            mover.velocity.limit(mover.topspeed)
            mover.move_vector(mover.velocity)

            board.run()

        .. raw:: html 

             <video loop autoplay muted width=240>
            <source src="../_static/mp4/vector_1.mp4" type="video/mp4">
            <source src="../_static/vector_1.webm" type="video/webm">
            Your browser does not support the video tag.
            </video> 

    """

    def __init__(self, x: float, y: float):
        self.vec = np.array([x, y])

    def __getitem__(self, item):
        if item == 0:
            return self.vec[0]
        else:
            return self.vec[1]

    @property
    def angle(self):
        """describes the angle as miniworldmaker direction"""
        return self.to_direction()

    @property
    def x(self) -> float:
        """the x compoonent of the vector"""
        return self.vec[0]

    @x.setter
    def x(self, value: float):
        self.vec = np.array([value, self.vec[1]])

    @property
    def y(self) -> float:
        """the y component of the vector"""
        return self.vec[1]

    @y.setter
    def y(self, value: float):
        self.vec = np.array([self.vec[0], value])

    @classmethod
    def from_positions(cls, p1: Union["board_position.Position",tuple], p2: Union["board_position.Position",tuple]) -> "Vector":
        """Create a vector from token and position

        The vector desribes is generated from:
        token2.center - position
        """
        p1 = board_position.Position.create(p1)
        p2 = board_position.Position.create(p2)
        x = p2.x - p1.x
        y = p2.y - p1.y
        return cls(x, y)

    @classmethod
    def from_token_and_position(cls, t1: "token_mod.Token", pos) -> "Vector":
        """Create a vector from token and position

        The vector desribes is generated from:
        token2.center - position
        """
        x = pos[0] - t1.center.x
        y = pos[1] - t1.center.y
        return cls(x, y)

    @classmethod
    def from_tokens(cls, t1: "token_mod.Token", t2: "token_mod.Token") -> "Vector":
        """Create a vector from two tokens.

        The vector desribes is generated from:
        token2.center - token1.center
        """
        x = t2.center.x - t1.center.x
        y = t2.center.y - t1.center.y
        return cls(x, y)

    @classmethod
    def from_direction(cls, direction: Union[str, int, float, str, "board_direction.Direction"]) -> "Vector":
        """Creates a vector from miniworldmaker direction."""
        if direction >= 90:
            x = 0 + math.sin(math.radians(direction)) * 1
            y = 0 - math.cos(math.radians(direction)) * 1
        else:
            x = 0 + math.sin(math.radians(direction)) * 1
            y = 0 - math.cos(math.radians(direction)) * 1
        return cls(x, y)

    @classmethod
    def from_token_direction(cls, token: "token_mod.Token") -> "Vector":
        """Creates a vector from token direction

        Examples:

            Creates rotating rectangle

            .. code-block:: python

                from miniworldmaker import *

                board = Board()

                player = Rectangle((200,200),40, 40)
                player.speed = 1
                player.direction = 80

                @player.register
                def act(self):
                    v1 = Vector.from_token_direction(self)
                    v1.rotate(-1)
                    self.direction = v1

                board.run()

        .. raw:: html 

             <video loop autoplay muted width="400">
            <source src="../_static/mp4/rotating_rectangle.mp4" type="video/mp4">
            <source src="../_static/rotating_rectangle.webm" type="video/webm">
            Your browser does not support the video tag.
            </video> 
        """
        return Vector.from_direction(token.direction)

    @classmethod
    def from_token_position(cls, token: "token_mod.Token") -> "Vector":
        """Creates a vector from token position"""
        x = token.center.x
        y = token.center.y
        return cls(x, y)

    def rotate(self, theta: float) -> "Vector":
        """rotates Vector by theta degrees"""
        theta_deg = theta % 360
        theta = np.deg2rad(theta_deg)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        self.vec = np.dot(rot, self.vec)
        return self

    def to_direction(self) -> float:
        """Returns miniworldmaker direction from vector."""
        if self.x > 0:
            axis = np.array([0, -1])
        else:
            axis = np.array([0, 1])
        unit_vector_1 = self.vec / np.linalg.norm(self.vec)
        unit_vector_2 = axis / np.linalg.norm(axis)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        angle = np.rad2deg(angle)
        if self.x > 0:
            return angle
        else:
            return angle + 180

    def get_normal(self):
        self.vec = np.array([- self.vec[1], self.vec[0]])
        return self

    def normalize(self) -> "Vector":
        """sets length of vector to 1

        Examples:

            Normalized vector with length 1:

            .. code-block:: python

                w = Vector(4, 3)
                print(w.length())     # 5
                print(w.normalize()) #  (0.8, 0.6)
        """
        norm = np.linalg.norm(self.vec)
        if norm == 0:
            self.vec = (0, 0)
            return self
        self.vec = self.vec / norm
        return self

    def length(self) -> float:
        """returns length of vector

        Examples:

            Length of vector

            .. code-block:: python

                w = Vector(4, 3)
                print(w.length())     # 5

        """
        return np.linalg.norm(self.vec)

    def neg(self) -> "Vector":
        """returns -v for Vector v

        Examples:

            Inverse of vector:

            .. code-block:: python

                u = Vector(2, 4)
                print(u.neg()) # (-2, 5)

            Alternative:

            .. code-block:: python

                print(- u)  # (-2, 5)

        """
        x = -self.x
        y = -self.y
        self.x, self.y = x, y
        return self

    def multiply(self, other: Union[float, "Vector"]) -> Union[float, "Vector"]:
        """product self * other:
        * returns product, if ``other`` is scalar (return-type: Vector)
        * returns dot-product, if ``other`` is vector (return-type: float)
        Args:
            other : a scalar or vector


        Examples:

            Product and dot-product:

            .. code-block:: python

                a = 5
                u1 = Vector(2, 4)
                u2 = Vector(2, 4)
                v = Vector(3, 1)
                print(u1.multiply(a)) # (10, 25)
                print(u2.multiply(v)) # 11

            Alternative:

            .. code-block:: python

                print(u1 * a)  # 25
                print(u1 * v) # 25
        """
        if type(other) in [int, float]:
            x = self.x * other
            y = self.y * other
            self.x, self.y = x, y
            return Vector(x, y)
        if type(other) == Vector:
            dot_product = self.dot(other)
            return dot_product

    def dot(self, other: "Vector") -> "Vector":
        self.vec = np.dot(self.vec, other.vec)
        return self

    def add_to_position(self, position: "board_position.Position") -> "board_position.Position":
        position = board_position.Position.create(position)
        return board_position.Position.create((self.x + position.x, self.y + position.y))

    def __str__(self):
        return f"({round(self.x, 3)},{round(self.y, 3)})"

    def __neg__(self):
        return self.neg()

    def __mul__(self, other: Union[int, float, "Vector"]) -> "Vector":
        if type(other) in [int, float]:
            x = self.x * other
            y = self.y * other
            return Vector(x, y)
        if type(other) == Vector:
            dot_product = self.dot(other)
            self.vec = dot_product
            return self

    def __add__(self, other: "Vector") -> "Vector":
        if type(other) == Vector:
            x = self.x + other.x
            y = self.y + other.y
            return Vector(x, y)

    def __sub__(self, other: "Vector") -> "Vector":
        if type(other) == Vector:
            x = self.x - other.x
            y = self.y - other.y
            return Vector(x, y)

    def sub(self, other: "Vector") -> "Vector":
        """adds vector `other` from self.

        Args:
            other (Vector): other Vector

        Returns:
            `self` + `other`

        Examples:

            Subtracts two vectors:

            .. code-block:: python

                v = Vector(3, 1)
                u = Vector(2, 5)
                print(u.sub(v)) # (1, -4)


            Alternative:

            .. code-block:: python

                print(u - v)
        """
        if type(other) == Vector:
            x = self.x - other.x
            y = self.y - other.y
            self.x, self.y = x, y
            return self

    def add(self, other: "Vector") -> "Vector":
        """adds vector `other` to self.

        Args:
            other (Vector): other Vector

        Returns:
            `self` + `other`

        Examples:

            Add two vectors:

            .. code-block:: python

                v = Vector(3, 1)
                u = Vector(2, 5)
                print(u.add(v)) # (5, 6)


            Alternative:

            .. code-block:: python

                print(u + v)
        """
        if type(other) == Vector:
            x = self.x + other.x
            y = self.y + other.y
            self.x, self.y = x, y
            return self

    def limit(self, value: float) -> "Vector":
        """limits length of vector to value"""
        if self.length() > value:
            self.normalize().multiply(value)
        return self
