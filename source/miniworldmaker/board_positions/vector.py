from miniworldmaker import token
import math
from miniworldmaker.board_positions import board_position_factory
class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def from_tokens(self, t1, t2):
        self.x = t2.center - t1.center
        self.y = t2.center - t1.center

    def normalize(self):
        l = math.sqrt(self.x**2 +self.y**2)

    def add_to_position(self, position):
        position = board_position_factory.BoardPositionFactory.create(position)
        return (self.x + position.x, self.y + position.y) 
