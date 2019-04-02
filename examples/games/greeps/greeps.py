from miniworldmaker import *
from typing import *
from functools import reduce
import random


class Earth(PixelBoard):
    def __init__(self):
        super().__init__(rows=600, columns=800)
        self.add_image("images/worlds/map0.jpg")
        scores = list()
        self.ship = self.add_to_board(Ship((170, 100)), position=(30, 30))
        self.window.add_container(EventConsole(), "right", 500)
        self.speed = 100
        for i in range(50):
            self.add_to_board(Tomato(), position=(random.randint(0, 800), random.randint(0, 600)))

    def show_map(self, map_no):
        pass


class Ship(Actor):

    def __init__(self, target_position):
        super().__init__()
        self.add_image("images/spaceship.png")
        self.size = (80, 80)
        self.target_position = target_position
        self.greeps = 0

    def act(self):
        if self.position != self.target_position:
            self.point_towards_position(self.target_position)
            self.move()
        if self.greeps < 30 and self.position == self.target_position:
            self.board.add_to_board(Greep(), self.position)
            self.greeps += 1


class Tomato(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/tomato.png")

    def act(self):
        print(self.image, self.image.get_rect())


class Greep(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/greeps/greep.png")
        self.add_costume("images/greeps/greep_with_food.png")
        self.point_in_direction(random.randint(0, 360))
        self.carrys_tomato = False

    def move(self, distance: int = 1) -> BoardPosition:
        if self.is_valid_move():
            return super().move()

    def is_looking_at_water(self):
        if self.is_sensing_color((40, 60, 120, 255), distance=1) < 1:
            return False
        else:
            return True

    def is_looking_on_board(self):
        if self.sensing_on_board(distance=1):
            return True
        else:
            return False

    def is_valid_move(self):
        if not self.is_looking_at_water() and self.is_looking_on_board():
            return True
        else:
            return False

    def act(self):
        if self.is_valid_move():
            self.move()
        else:
            if self.carrys_tomato:
                self.point_towards_position(self.board.ship.position)
                # self.turn_left(random.randint(-20,20))
            else:
                self.turn_left(random.randint(90, 270))
        greep = self.sensing_token(token=Greep)
        tomato = self.sensing_token(token=Tomato)
        if greep and tomato:
            self.charge(greep, tomato)
            greep.switch_costume()
        if self.carrys_tomato:
            print("turn home")
            self.turn_home()
            if self.sensing_token(token=Ship):
                self.remove()

    def charge(self, greep, tomato):
        if greep and tomato:
            print("charging")
            greep.carrys_tomato = True
            tomato.remove()

    def turn_home(self):
        self.point_towards_position(self.board.ship.position)


earth = Earth()
earth.show()
