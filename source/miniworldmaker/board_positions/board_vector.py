from miniworldmaker.tokens import token
import math
from miniworldmaker.board_positions import board_position_factory
class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_tokens(cls, t1, t2):
        x = t2.center.x - t1.center.x
        y = t2.center.y - t1.center.y
        return cls(x, y)

    def normalize(self):
        l = math.sqrt(self.x**2 +self.y**2)
        if l == 0:
            return 0
        self.x = self.x/l
        self.y = self.y/l
        return self
    
    def length(self):
        l = math.sqrt(self.x**2 +self.y**2)
        return l
    
    def neg(self):
        self.x = - self.x
        self.y = - self.y
        return self

    def multiply(self, value):
        self.x = self.x * value
        self.y = self.y * value
        return self
        
    def add_to_position(self, position):
        position = board_position_factory.BoardPositionFactory().create(position)
        return (self.x + position.x, self.y + position.y) 

    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __neg__(self):
        return self.neg()
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return self.multiply(value)
    
    