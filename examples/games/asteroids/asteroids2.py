from miniworldmaker import *
import random


class MyBoard(PixelBoard):

    def __init__(self, screen_x, screen_y):
        super().__init__(columns=screen_x, rows=screen_y)
        asteroids = list()
        for i in range(5):
            asteroid = self.add_to_board(Asteroid(),
                                         position=(random.randint(60, screen_x - 30),
                                                   random.randint(60, screen_y - 30)))
            asteroids.append(asteroid)
        self.player = self.add_to_board(Player(), position=(20, 120))
        self.add_image("images/galaxy.jpg")
        # Preload explosion for faster image handling
        explosion = Explosion()


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/ship.png")
        self.size = (30,30)
        self.costume.orientation = - 90

    def get_event(self,event, data):
        if event == "key_pressed":
            if "W" in data:
                self.turn_left(10)
            elif "S" in data:
                self.turn_right(10)
        if event == "key_down":
            if "SPACE" in data:
                self.shoot()

    def act(self):
        self.move()
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
        if self.sensing_token(token=Asteroid, exact= True):
            explosion = self.board.add_to_board(Explosion(), position=self.position.up(40).left(40))
            explosion.costume.is_animated = True
            self.board.play_sound("sounds/explosion.wav")
            self.remove()

    def shoot(self):
        laser = Laser(self.direction)
        self.board.add_to_board(laser, self.position.down(10))


class Laser(Actor):
    def __init__(self, direction):
        super().__init__()
        self.add_image("images/laser.png")
        self.size = (30, 30)
        self.direction = direction
        self.costume.orientation = 180
        self.speed = 15

    def add_to_board(self, board, position):
        super().add_to_board(board, position)
        self.board.play_sound("sounds/laser.wav")

    def act(self):
        self.move()
        token = self.sensing_token(token = Asteroid, exact = True)
        if token:
            token.remove()
            explosion = self.board.add_to_board(Explosion(), position=token.position.up(40).left(40))
            explosion.costume.is_animated = True
            explosion.costume.text_position = (100,100)
            explosion.costume.text = "100"
            self.board.play_sound("sounds/explosion.wav")
            self.remove()


class Asteroid(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/asteroid.png")
        self.size = (30, 30)
        self.direction = random.randint(0, 360)

    def act(self):
        borders = self.sensing_borders()
        if borders:
            self.bounce_from_border(borders)
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