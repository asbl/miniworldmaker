from gamegridp import actor
import numpy as np
import math


class PhysicsActor(actor.Actor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vector = np.array([1,0])
        self._exact_coordinates = np.array([self.cell[0]+0.0, self.cell[1]+0.0])

    def bounce_from_border(self):
        borders = self.touching_borders
        if "top" in borders:
            self._vector[1] *= -1
        elif "bottom" in borders:
            self._vector[1] *= -1
        elif "left" in borders:
            self._vector[0] *= -1
        elif "right" in borders:
            self._vector[0] *= -1

    @staticmethod
    def _unit_vector(vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    @staticmethod
    def _angle_between(v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::
        """
        v1_u = PhysicsActor._unit_vector(v1)
        v2_u = PhysicsActor._unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def move(self, distance=1, direction = "forward"):
        self._exact_coordinates[0] = self._exact_coordinates[0] + self._vector[0]+0.0
        self._exact_coordinates[1] = self._exact_coordinates[1] + self._vector[1]+0.0
        print("Vector :", self._vector)
        print(self._exact_coordinates)
        self.set_x(round(self._exact_coordinates[0]))
        self.set_y(round(self._exact_coordinates[1]))
        print("Cell :",self.cell[0],self.cell[1])

    def inc_speed(self, factor):
        self._vector *= factor

    def dec_speed(self, factor):
        self._vector /= factor

    @property
    def direction(self) -> int:
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return super().direction

    @direction.setter
    def direction(self, value):
        print("Value-Type",type(value))
        print("Value", value)
        direction = np.degrees(PhysicsActor._angle_between(np.array([1, 0]), value))
        print("Direction in physics actor:", direction)
        if self._vector[1] > 0:
            self._direction = 360 - direction
        else:
            self._direction = direction

    def set_direction_by_vector(self):
        self.direction = self._vector

    def set_vector_by_direction(self):
        self._vector = np.array([1, 0])
        self.turn_left(self.direction)

    @staticmethod
    def rotate_vector(self, vector, degrees, clockwise=False):
        deg = np.radians(degrees)
        c, s = np.cos(deg), np.sin(deg)
        if clockwise: #turn right
            turn_matrix = np.array(((c, s), (-s, c)))
        else:  # turn left
            turn_matrix = np.array(((c, -s), (s, c)))
        return np.dot(vector, turn_matrix)

    def get_vector_by_direction(self, direction):
        return PhysicsActor.rotate_vector(np.array([1, 0]), direction)

    def turn_left(self, deg):
        self._vector = self.rotate_vector(self._vector, deg)

    def turn_right(self, deg):
        self._vector = self.rotate_vector(self._vector, deg, clockwise=True)

    def bounce_from_line(self, line_angle):
        self.direction = (line_angle * 2 - self.direction) % 360

    def bounce_from_actor(self, actor):
        mirror_angle = (self.direction + actor.direction) / 2
        self.bounce_from_line(mirror_angle)

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        if value != self._vector:
            self._vector = value
            self.set_vector_by_direction(value)

