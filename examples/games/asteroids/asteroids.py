from miniworldmaker import *
import random


class MyBoard(PixelBoard):

    def __init__(self, screen_x, screen_y):
        super().__init__(columns=screen_x, rows=screen_y)
        asteroids = list()
        for i in range(5):
            asteroid = Asteroid( position=(random.randint(30, screen_x - 30),
                                                   random.randint(0 + 30, screen_y - 30))),
            asteroids.append(asteroid)
        Player(position=(40, 40))
        self.add_image("images/galaxy.jpg")


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/ship.png")
        self.size = (30,30)
        self.direction = 90
        self.costume.orientation = - 90

    def get_event(self,event, data):
        if event == "key_pressed":
            if "W" in data:
                self.turn_left(10)
            elif "S" in data:
                self.turn_right(10)

    def act(self):
        self.move()
        if not self.sensing_on_board():
            self.turn_left(180)
        if self.sensing_token(token=Asteroid):
            explosion = self.board.add_to_board(Explosion(), position=self.position)
            explosion.costume.is_animated = True
            self.board.play_sound("sounds/explosion.wav")
            self.remove()


class Asteroid(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/asteroid.png")
        self.size = (30, 30)
        self.direction = random.randint(0, 360)

    def act(self):
        if not self.sensing_on_board():
            self.turn_left(180)
        else:
            self.move()


class Explosion(Actor):
    def __init__(self):
        super().__init__()
        self.size = (128,128)
        self.add_image("images/explosion00.png")
        self.add_image("images/explosion01.png")
        self.add_image("images/explosion02.png")
        self.add_image("images/explosion03.png")
        self.add_image("images/explosion04.png")
        self.add_image("images/explosion05.png")
        self.add_image("images/explosion06.png")
        self.add_image("images/explosion07.png")
        self.add_image("images/explosion08.png")
        self.costume.animation_speed = 3
        self.counter = 0

    def act(self):
        self.counter+= 1
        if self.counter == 8:
            self.remove()


random.seed()
my_board = MyBoard(400, 300)
my_board.show()