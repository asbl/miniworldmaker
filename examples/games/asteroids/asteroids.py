from gamegridp import *
import random


class MyGrid(PixelGrid):

    def __init__(self):
        super().__init__( cell_size=1, columns=screen_x, rows=screen_y,
                margin=0)
        asteroids = list()
        for i in range(5):
            asteroid = self.add_actor(Asteroid(), position = (random.randint(30,screen_x-30),random.randint(0+30,screen_y-30)))
            asteroids.append(asteroid)
        self.player = self.add_actor(Player(), position = (40,40))
        for asteroid in asteroids:
            self.add_collision_partner(self.player,asteroid)
        self.add_image("images/galaxy.jpg")

    def get_event(self, event, data):
        if event == "collision":
            partner1, partner2 = data[0], data[1]
            position = partner1.position
            partner1.remove()
            partner2.remove()
            self.add_actor(Explosion(), position=position)
            self.stop()


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
        if not self.grid.is_in_grid(self.look(distance = 4, direction="forward", )):
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
mygrid.show_log()
mygrid.show()
