import random

from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self, screen_x, screen_y):
        super().__init__(columns=screen_x, rows=screen_y)
        asteroids = list()
        for i in range(5):
            asteroid = Asteroid(position=(random.randint(30, screen_x - 30),
                                          random.randint(0 + 30, screen_y - 30))),
            asteroids.append(asteroid)
        Player(position=(40, 40))
        self.add_image("images/galaxy.jpg")


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/ship.png")
        self.size = (30, 30)
        self.costume.orientation = - 90

    def on_key_pressed(self, keys):
        if "W" in keys:
            self.turn_left(10)
        elif "S" in keys:
            self.turn_right(10)

    def on_key_down(self, keys):
        if "SPACE" in keys:
            self.shoot()

    def act(self):
        self.move()
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
        if self.sensing_token(token_type=Asteroid):
            explosion = Explosion(position=self.position.up(40).left(40))
            explosion.costume.is_animated = True
            self.board.play_sound("sounds/explosion.wav")
            self.remove()

    def shoot(self):
        laser = Laser.from_center(self.center)
        laser.direction = self.direction


class Laser(Actor):

    def on_setup(self):
        self.add_image("images/laser.png")
        self.size = (30, 30)
        self.costume.is_upscaled = True
        self.costume.orientation = 180
        self.speed = 15
        self.board.play_sound("sounds/laser.wav")
        print("shoot laser" + str(self.board ) )

    def act(self):
        self.move()

    def on_sensing_asteroid(self, other):
        print("laser hitting board",  self.board)
        print(self, other)
        other.remove()
        explosion = Explosion(position=other.position.up(40).left(40))
        explosion.costume.is_animated = True
        explosion.costume.text_position = (100, 100)
        explosion.costume.text = "100"
        self.board.play_sound("sounds/explosion.wav")
        self.remove()


class Asteroid(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/asteroid.png")
        self.size = (30, 30)
        self.direction = random.randint(0, 360)

    def act(self):
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
        self.move()


class Explosion(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.size = (128, 128)
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
        self.counter += 1
        if self.counter == 8:
            self.remove()


random.seed()
my_board = MyBoard(400, 300)
my_board.show()
