from miniworldmaker import *
import random


class MyGrid(PixelBoard):

    def __init__(self):
        super().__init__(columns=screen_x, rows=screen_y)
        asteroids = list()
        for i in range(5):
            asteroid = self.add_to_board(Asteroid(), board_position=(
            random.randint(30, screen_x - 30), random.randint(0 + 30, screen_y - 30)))
            asteroids.append(asteroid)
        self.player = self.add_to_board(Player(), board_position=(40, 40))
        for asteroid in asteroids:
            self.add_collision_partner(self.player,asteroid)
        self.add_image("images/galaxy.jpg")

    def get_event(self, event, data):
        if event == "collision":
            partner1, partner2 = data[0], data[1]
            position = partner1.position
            partner1.remove()
            partner2.remove()
            self.add_to_board(Explosion(), board_position=position)
            self.is_running = False


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/ship.png")
        self.size = (30,30)

    def get_event(self,event, data):
        if event == "key":
            if "W" in data:
                self.turn_left(10)
            elif "S" in data:
                self.turn_right(10)

    def act(self):
        self.move(distance = 3)


class Asteroid(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/asteroid.png")
        self.size = (30, 30)
        self.direction = random.randint(0, 360)
        self.image_action("info_overlay", True)

    def act(self):
        if not self.is_looking_on_board(direction="forward", distance=4):
            self.turn_left(180)
        else:
            self.move(distance = 4, direction = "forward")

class Explosion(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/explosion.png")

random.seed()
screen_x=400
screen_y=300
mygrid = MyGrid()
mygrid.speed = 60
mygrid.show()
