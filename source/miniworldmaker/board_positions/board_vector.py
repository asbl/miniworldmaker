from miniworldmaker.tokens import token
import math
from miniworldmaker.board_positions import board_position_factory
from miniworldmaker.board_positions import board_position
import numpy as np
import math
class Vector:
    """Describes a two dimensional vector.

    It is used to describe a position, acceleration
    or velocity.
    """

    def __init__(self, x, y):
        self.vec = np.array([x,y])

    @property    
    def angle(self):
        """describes the angle as miniworldmaker direction
        """
        return self.to_direction()

    @property
    def x(self):
        """the x compoonent of the vector
        """
        return self.vec[0]

    @x.setter
    def x(self, value):
        self.vec[0]= value
    
    @property
    def y(self):
        """the y component of the vector
        """
        return self.vec[1]

    @y.setter
    def y(self, value):
        self.vec[1]= value
    
    @classmethod
    def from_tokens(cls, t1, t2):
        """Create a vector from two tokens.

        The vector desribes is generated from:
        token2.center - token1.center
        """
        x = t2.center.x - t1.center.x
        y = t2.center.y - t1.center.y
        return cls(x, y)

    @classmethod
    def from_dir(cls, direction):
        """Creates a vector from miniworldmaker direction.
        """
        x = 0 + math.sin(math.radians(direction)) * 1
        y = 0 - math.cos(math.radians(direction)) * 1
        return cls(x, y)

    @classmethod
    def from_token_direction(cls, token):
        """Creates a vector from token direction
        """
        x = math.sin(math.radians(token.direction)) * 1
        y = math.cos(math.radians(token.direction)) * 1
        return cls(x, y)

    @classmethod
    def from_token_position(cls, token):
        """Creates a vector from token position
        """
        x = token.center.x
        y = token.center.y
        return cls(x, y)


    def rotate(self, theta : float) -> "Vector":
        """rotates Vector by theta degrees
        """
        theta_deg = theta % 360
        theta = np.deg2rad(theta_deg)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        vec = self.vec
        self.vec = np.dot(rot, self.vec)
        return self

    def to_direction(self) -> float:
        """Returns miniworldmaker direction from vector.
        """
        if self.x > 0:
            axis = np.array([0, -1])
        else:
            axis = np.array([0,1])
        unit_vector_1 = self.vec / np.linalg.norm(self.vec)
        unit_vector_2 = axis / np.linalg.norm(axis)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        angle = np.rad2deg(angle)
        if self.x > 0:
            return angle
        else:
            return angle + 180

    def normalize(self) -> "Vector":
        """sets length of vector to 1"""
        l = np.linalg.norm(self.vec)
        if l == 0:
            return 0
        self.vec = self.vec / l
        return self
    
    def length(self) -> float:
        """returns length of vector"""
        return np.linalg.norm(self.vec)
    
    def neg(self) -> "Vector":
        """returns -v for Vector v
        """
        self.x = - self.x
        self.y = - self.y
        return self

    def multiply(self, value : float) -> "Vector":
        """returns a * v
          * a is a scalar
          * v is a vector

        Args:
            value (float): a scalar

        Returns:
            Vector: the vector a*v
        """
        self.x = self.x * value
        self.y = self.y * value
        return self
        
    def add_to_position(self, position : "board_position.BoardPosition") -> "board_position.BoardPosition":
        position = board_position_factory.BoardPositionFactory().create(position)
        return board_position_factory.BoardPositionFactory().create((self.x + position.x, self.y + position.y))

    def __str__(self):
        return f"({round(self.x,3)},{round(self.y,3)})"
    
    def __neg__(self):
        return self.neg()
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return self.multiply(other)
    
    def __sub__(self, other):
        if type(other) == Vector:
            x = self.x - other.x
            y = self.y - other.y
            return Vector(x, y)

    def sub(self, other : "Vector") -> "Vector":
        """adds vector `other` from self.

        Args:
            other (Vector): other Vector

        Returns:
            Vector: `self` + `other`
        """
        if type(other) == Vector:
            self.x = self.x - other.x
            self.y = self.y - other.y
            return self

    def add(self, other : "Vector") -> "Vector":
        """subtracts vector `other` from self.

        Args:
            other (Vector): other Vector

        Returns:
            Vector: `self` - `other`
        """
        if type(other) == Vector:
            self.x = self.x + other.x
            self.y = self.y + other.y
            return self

    def limit(self, value : float):
        """limits length of vector to value
        """
        if self.length() > value:
            self.normalize().multiply(value)