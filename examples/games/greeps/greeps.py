import random

from miniworldmaker import *


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
        self.water_colors = [(49, 84, 130, 255),
                             (49, 84, 129, 255),
                             (50, 84, 129, 255),
                             (44, 84, 133, 255),
                             (41, 84, 127, 255),
                             (49, 94, 136, 255),
                             (56, 88, 129, 255),
                             ]

    def show_map(self, map_no):
        pass

    def act(self):
        time = 500
        if (self.frame > time and self.index <= 2):
            self.is_running = False
            for token in self.tokens:
                token.remove()
            self.background.next_image()
            self._repaint_all = 1
            self.dirty = 1
            self.index += 1
        if (self.index == 0 and self.frame == 1) or (self.frame > time and self.index <= 2):
            self.create_new_world()

    def create_new_world(self):
        print("create new world")
        self.is_running = False
        self.frame = 0
        for tomatopile in self.tomato_piles[self.index]:
            position = (tomatopile[1], tomatopile[2])
            Tomatos(position = position, number = tomatopile[0])
        position = (self.ship_pos[self.index][1], self.ship_pos[self.index][0])
        self.ship = Ship(position=self.target[self.index], target_position=position)
        self.greeps = 0
        self.is_running = True
        self.index += 1


class Ship(Actor):

    def on_setup(self, target_position):
        print("setup")
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
        if self.greeps < 20 and self.center.near(self.target_position, self.speed):
            self.stop = True
            Greep(self.position)
            self.greeps += 1

class Tomatos(Token):

    def on_setup(self, number):
        print("tomato setup")
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

    def on_setup(self):
        self.orientation = - 90
        self.add_image("images/greeps/greep.png")
        self.add_costume("images/greeps/greep_with_food.png")
        self.size = (35, 35)
        self.point_in_direction(random.randint(0, 360))
        self.carrys_tomato = False
        self.memory = 0
        self.speed = 5

    def move(self, distance: int = 1) -> BoardPosition:
        if self.is_valid_move():
            return super().move()
        else:
            return None

    def is_looking_at_water(self):
        sensing_colors = self.sensing_colors(distance=10, colors=self.board.water_colors)
        if sensing_colors:
            return True
        else:
            return False

    def is_valid_move(self):
        if self.sensing_borders(distance=self.speed) or self.is_looking_at_water():
            return False
        else:
            return True

    def act(self):
        self.think()
        self.move()
        if not self.is_valid_move():
            self.turn_left(random.randint(120, 240))

    def think(self):
        self.memory = self.memory + 1
        if self.memory > 0 and self.memory % 40 == 0:
            if self.carrys_tomato:
                self.spit("red")
            else:
                self.spit("blue")

        greep = self.sensing_token(token_type=Greep, distance=0)
        tomato = self.sensing_token(token_type=Tomatos, distance=0)

        if greep and tomato:
            self.charge(greep, tomato)
            # self.point_towards_position(self.board.ship.position)
        if self.carrys_tomato:
            self.turn_home()
            if self.sensing_token(token_type=Ship, distance=0):
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
            paint = Paint(position = self.position, color = color)
        if color == "green":
            paint = Paint(position = self.position, color = color)
        if color == "blue":
            paint = Paint(position=self.position, color = color)



class Paint(Token):

    def on_setup(self, color):
        self.add_image("images/paint.png")
        self.intensity = 255
        self.costume.coloring = (255, 0, 0, self.intensity)
        self.time = 0
        self.color = color

    def update(self):
        super().update()
        self.time = self.time + 1
        if self.time % 50 == 0 and self.time > 0:
            self.intensity = self.intensity % 2
            if self.color == "red":
                self.costume.color((255, 0, 0, self.intensity))
            if self.color == "green":
                self.costume.color((0, 255, 0, self.intensity))
            if self.color == "blue":
                self.costume.color((0, 0, 255, self.intensity))
            self.dirty = 1
            if self.intensity < 50:
                self.remove()


earth = Earth()
earth.show()
