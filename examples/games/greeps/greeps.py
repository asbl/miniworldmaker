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
        toolbar = Toolbar()
        self.window.add_container(toolbar, "right", 400)
        self.counter = toolbar.add_widget(CounterLabel("Tomatoes in first world"))
        self.time_label = toolbar.add_widget(TimeLabel(self, "Time"))
        self.time_label = toolbar.add_widget(FPSLabel(self, "FPS"))
        self.speed = 100
        for i in range(40):
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
        self.costume.overlay = True

    def act(self):
        if self.position != self.target_position:
            self.point_towards_position(self.target_position)
            self.move()
        if self.greeps < 80 and self.position == self.target_position:
            self.board.add_to_board(Greep(), self.position)
            self.greeps += 1


class Tomato(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/tomato.png")


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
            greep = self.sensing_token(token=Greep, distance=0)
            tomato = self.sensing_token(token=Tomato, distance=0)
            if greep and tomato:
                self.charge(greep, tomato)
                greep.switch_costume()
                # self.point_towards_position(self.board.ship.position)
            if self.carrys_tomato:
                self.turn_home()
                if self.sensing_token(token=Ship, distance=0):
                    board = self.board
                    self.remove()
                    board.counter.add(1)
        else:
            self.turn_left(random.randint(120, 240))



    def charge(self, greep, tomato):
        if greep and tomato:
            greep.carrys_tomato = True
            tomato.remove()

    def turn_home(self):
        self.point_towards_position(self.board.ship.position)


def main():
    earth = Earth()
    earth.show()


import cProfile

pr = cProfile.Profile()
pr.enable()
main()
pr.disable()
pr.dump_stats("profile")
