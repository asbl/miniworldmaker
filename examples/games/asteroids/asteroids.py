import random

import miniworldmaker as mwm


class MyBoard(mwm.PixelBoard):

    def on_setup(self):
        asteroids = list()
        for i in range(5):
            asteroid = Asteroid(position=(random.randint(30, self.width - 30),
                                          random.randint(0 + 30, self.height - 30))),
            asteroids.append(asteroid)
        Player(position=(40, 40))
        self.add_background("images/galaxy.jpg")


class Player(mwm.Token):

    def __init__(self, position):
        super().__init__(position)
        self.add_costume("images/ship.png")
        self.size = (30, 30)
        self.costume.orientation = - 90

    def on_key_pressed_w(self):
        self.turn_left(10)

    def on_key_pressed_s(self):
        self.turn_right(10)

    def on_key_down_space(self):
        self.shoot()

    def act(self):
        self.move()
        borders = self.sensing_borders()

    def on_sensing_asteroid(self, asteroid):
        explosion = Explosion(position=self.position.up(40).left(40))
        explosion.costume.is_animated = True
        self.board.play_sound("sounds/explosion.wav")
        self.remove()

    def on_sensing_borders(self, borders):
        self.bounce_from_border(borders)

    def shoot(self):
        laser = Laser.from_center(self.position)
        laser.direction = self.direction


class Laser(mwm.Token):

    def on_setup(self):
        self.add_costume("images/laser.png")
        self.size = (30, 30)
        self.costume.is_upscaled = True
        self.costume.orientation = 180
        self.speed = 15
        self.board.play_sound("sounds/laser.wav")

    def act(self):
        self.move()

    def on_sensing_asteroid(self, other):
        other.remove()
        explosion = Explosion(position=other.position.up(40).left(40))
        explosion.costume.is_animated = True
        explosion.costume.text_position = (100, 100)
        explosion.costume.text = "100"
        self.board.play_sound("sounds/explosion.wav")
        self.remove()


class Asteroid(mwm.Token):
    def __init__(self, position):
        super().__init__(position)
        self.add_costume("images/asteroid.png")
        self.size = (30, 30)
        self.direction = random.randint(0, 360)

    def act(self):
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
        self.move()


class Explosion(mwm.Token):

    def on_setup(self):
        self.size = (128, 128)
        self.add_costume()
        self.costume.add_images(["images/explosion00.png",
                                "images/explosion01.png",
                                "images/explosion02.png",
                                "images/explosion03.png",
                                "images/explosion04.png",
                                "images/explosion05.png",
                                "images/explosion06.png",
                                "images/explosion07.png",
                                "images/explosion08.png"]
                                )
        self.costume.animation_speed = 10
        self.costume.is_animated = True
        mwm.ActionTimer(24, self.remove, None)


random.seed()
my_board = MyBoard(400, 300)
my_board.run()
