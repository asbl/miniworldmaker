from miniworldmaker import *
from typing import *
from functools import reduce
import random



class Earth(PixelBoard):
    def __init__(self):
        super().__init__(rows=600, columns=800)
        self.index = 0
        self.add_image("images/worlds/map0.jpg")
        self.add_image("images/worlds/map1.jpg")
        self.add_image("images/worlds/map2.jpg")
        toolbar = Toolbar()
        self.window.add_container(toolbar, "right", 400)
        self.counter = []
        self.counter.append(toolbar.add_widget(CounterLabel("Tomatoes in 1. world")))
        self.counter.append(toolbar.add_widget(CounterLabel("Tomatoes in 2. world")))
        self.counter.append(toolbar.add_widget(CounterLabel("Tomatoes in 3. world")))
        self.counter.append(toolbar.add_widget(CounterLabel("Tomatoes total")))
        self.tomato_piles = []
        self.tomato_piles.append([[40, 721, 532], [12, 400, 560], [40, 615, 400],
                                  [40, 642, 192], [16, 128, 113], [30, 400, 40]], )
        self.tomato_piles.append([[10, 322, 422], [40, 700, 241], [40, 681, 49],
                                  [10, 317, 54], [50, 90, 174], [40, 60, 339]])
        self.tomato_piles.append([[10, 39, 30], [30, 71, 476], [50, 398, 520],
                                  [40, 655, 492]])
        self.ship_pos = []
        self.ship_pos.append([480, 100])
        self.ship_pos.append([496, 709])
        self.ship_pos.append([272, 394])
        self.target = []
        self.target.append((30, 30))
        self.target.append((20, 30))
        self.target.append((20, 30))
        self.time_label = toolbar.add_widget(TimeLabel(self, "Time"))

    def show_map(self, map_no):
        pass

    def act(self):
        time = 500
        if (self.frame > time and self.index <= 2):
            self.is_running = False
            for token in self.tokens:
                token.remove()
            self.background.next_sprite()
            self.dirty = 1
            self.index += 1
        if (self.index == 0 and self.frame == 1) or (self.frame > time and self.index <= 2):
            self.is_running = False
            self.frame = 0
            for tomatopile in self.tomato_piles[self.index]:
                tomatos = Tomatos(tomatopile[0])
                position = (tomatopile[1], tomatopile[2])
                self.add_to_board(tomatos, position)
            position = (self.ship_pos[self.index][1], self.ship_pos[self.index][0])
            self.ship = self.add_to_board(Ship(position), position=self.target[self.index])
            self.greeps = 0

            self.is_running = True




class Ship(Actor):

    def __init__(self, target_position):
        super().__init__()
        self.add_image("images/spaceship.png")
        self.size = (80, 80)
        self.target_position = target_position
        self.greeps = 0
        self.costume.is_rotatable = False
        self.speed = 20
        self.stop = False


    def act(self):
        if self.position != self.target_position and not self.stop:
            self.point_towards_position(self.target_position)
            self.move()
        if self.greeps < 20 and self.position.near(self.target_position, self.speed):
            self.stop = True
            self.board.add_to_board(Greep(), self.position)
            self.greeps += 1


class Tomatos(Token):
    def __init__(self, number):
        super().__init__()
        self.size = (40, 40)
        self.number = number
        for i in range(self.number // 10):
            self.add_image("images/tomatopile{0}.png".format(self.number // 10 - (i)))

    def get_tomato(self) -> int:
        self.number -= 1
        if self.number == 1:
            if self.number % 10 == 0:
                self.remove()
        return 1



class Greep(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/greeps/greep.png")
        self.add_costume("images/greeps/greep_with_food.png")
        self.size = (35, 35)
        self.point_in_direction(random.randint(0, 360))
        self.carrys_tomato = False
        self.memory = 0
        self.speed = 5
        self.costume.orientation = - 90

    def move(self, distance: int = 1) -> BoardPosition:
        if self.is_valid_move():
            return super().move()

    def is_looking_at_water(self):
        if self.sensing_color((40, 60, 120, 255), distance=self.speed) < 1:
            return False
        else:
            return True

    def is_looking_on_board(self):
        if self.sensing_on_board(distance=self.speed):
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
            self.think()
            self.move()
        else:
            self.turn_left(random.randint(120, 240))

    def think(self):
        self.memory = self.memory + 1
        if self.memory > 0 and self.memory % 40 == 0:
            if self.carrys_tomato:
                self.spit("red")
            else:
                self.spit("blue")

        greep = self.sensing_token(token=Greep, distance=0)
        tomato = self.sensing_token(token=Tomatos, distance=0)

        if greep and tomato:
            self.charge(greep, tomato)
            # self.point_towards_position(self.board.ship.position)
        if self.carrys_tomato:
            self.turn_home()
            if self.sensing_token(token=Ship, distance=0):
                self.deliver_to_ship()

    def deliver_to_ship(self):
        print("deliver")
        if self.sensing_token(token=Ship, distance=0) and self.carrys_tomato:
            self.carrys_tomato = False
            self.switch_costume(0)
            print("delivered")
            board = self.board
            board.counter[board.index].add(1)
            board.counter[len(board.counter) - 1].add(1)


    def charge(self, greep, tomato):
        greep = self.sensing_token(token=Greep, distance=0)
        tomato = self.sensing_token(token=Tomatos, distance=0)
        print("charge", self, greep, tomato, greep.carrys_tomato)
        if greep and tomato:
            if not greep.carrys_tomato:
                greep.carrys_tomato = True
                tomato.get_tomato()
                greep.switch_costume(index=1)


    def turn_home(self):
        self.point_towards_position(self.board.ship.position)

    def spit(self, color):

        if color == "red":
            paint = Paint(color="red")
            self.board.add_to_board(paint, position=self.position)
        if color == "green":
            paint = Paint(color="green")
            self.board.add_to_board(paint, position=self.position)
        if color == "blue":
            paint = Paint(color="blue")
            self.board.add_to_board(paint, position=self.position)


class Paint(Token):
    def __init__(self, color):
        super().__init__()
        self.add_image("images/paint.png")
        self.intensity = 255
        self.costume.colorize((255, 0, 0, self.intensity))
        self.time = 0
        self.color = color

    def update(self):
        super().update()
        self.time = self.time + 1
        if self.time % 50 == 0 and self.time > 0:
            self.intensity = self.intensity % 2
            if self.color == "red":
                self.costume.colorize((255, 0, 0, self.intensity))
            if self.color == "green":
                self.costume.colorize((0, 255, 0, self.intensity))
            if self.color == "blue":
                self.costume.colorize((0, 0, 255, self.intensity))
            self.dirty = 1
            if self.intensity < 50:
                self.remove()




def main():
    earth = Earth()
    earth.show()


import cProfile

pr = cProfile.Profile()
pr.enable()
main()
pr.disable()
pr.dump_stats("profile")
