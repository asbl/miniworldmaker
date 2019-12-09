from miniworldmaker import *


class MyBoard(TiledBoard):
    def on_setup(self):
        self.tile_size = 30
        robot1 = Robot(position=(0, 0))
        robot1.add_image("images/robo_green.png")
        robot1.direction = "right"
        robot2 = Robot(position=(28, 0))
        robot2.add_image("images/robo_yellow.png")
        robot2.direction = "left"
        self.add_image(path="images/water.png")
        self.speed = 30

class Explosion(Token):
    def on_setup(self):
        self.add_image("images/explosion.png")


class Robot(Actor):
    def on_setup(self):
        self.costume.orientation = - 90

    def act(self):
        self.move()
        other = self.sensing_token(distance = 0, token_type=Robot)
        if other:
            explosion = Explosion(position=self.position)
            self.remove()
            other.remove()


board = MyBoard(29, 1)
board.show()
