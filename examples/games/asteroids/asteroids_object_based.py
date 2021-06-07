import random
from miniworldmaker import *

board = PixelBoard(400,300)
board.add_background("images/galaxy.jpg")
asteroids = []
for i in range(2):
    asteroid = Token(position=(random.randint(30, board.width - 30),
                                              random.randint(30, board.height - 30)))
asteroid.add_costume("images/asteroid.png")
asteroid.size = (30, 30)
asteroid.direction = random.randint(0, 360)
@asteroid.register
def act(self):
    borders = self.sensing_borders()
    if borders:
        self.bounce_from_border(borders)
    self.move()
asteroids.append(asteroid)

player = Token(position=(40, 40))
player.add_costume("images/ship.png")
player.size = (30, 30)
player.costume.orientation = - 90
@player.register
def on_key_pressed_w(self):
    self.turn_left(10)

@player.register
def on_key_pressed_s(self):
    self.turn_right(10)

@player.register
def on_key_down_space(self):
    self.shoot()

@player.register
def act(self):
    self.move()
    borders = self.sensing_borders()

@player.register
def on_sensing_token(self, token):
    if token in asteroids:
        explosion = Token(position=self.position.up(40).left(40))
        explosion.size = (128, 128)
        explosion.add_costume()
        explosion.costume.add_images(["images/explosion00.png",
                                "images/explosion01.png",
                                "images/explosion02.png",
                                "images/explosion03.png",
                                "images/explosion04.png",
                                "images/explosion05.png",
                                "images/explosion06.png",
                                "images/explosion07.png",
                                "images/explosion08.png"]
                                )
        explosion.costume.animation_speed = 10
        explosion.costume.is_animated = True
        ActionTimer(24, explosion.remove)
        board.play_sound("sounds/explosion.wav")
        self.remove()

@player.register
def on_sensing_borders(self, borders):
    self.bounce_from_border(borders)

@player.register
def shoot(self):
    laser = Token()
    laser.direction = self.direction
    laser.add_costume("images/laser.png")
    laser.center = self.position
    laser.size = (30, 30)
    laser.costume.is_upscaled = True
    laser.costume.orientation = 180
    laser.speed = 15
    laser.board.play_sound("sounds/laser.wav")
    @laser.register
    def act(self):
            self.move()
            
    @laser.register
    def on_sensing_token(self, other):
        if other in asteroids:
            other.remove()
            explosion = Token(position=self.position.up(40).left(40))
            explosion.size = (128, 128)
            explosion.add_costume()
            explosion.costume.add_images(["images/explosion00.png",
                                    "images/explosion01.png",
                                    "images/explosion02.png",
                                    "images/explosion03.png",
                                    "images/explosion04.png",
                                    "images/explosion05.png",
                                    "images/explosion06.png",
                                    "images/explosion07.png",
                                    "images/explosion08.png"]
                                    )
            explosion.costume.animation_speed = 10
            explosion.costume.is_animated = True
            board.play_sound("sounds/explosion.wav")
            ActionTimer(24, explosion.remove)
            self.remove()


random.seed()
board.run()
