from miniworldmaker import *


class MyBoard(TiledBoard):
    def __init__(self):
        super().__init__(tile_size=40, columns=29, rows=1, tile_margin=0)
        robot1 = Robot(position=(0, 0))
        robot1.add_image("images/robo_green.png")
        robot1.direction = "right"
        robot2 = Robot(position=(28, 0))
        robot2.add_image("images/robo_yellow.png")
        robot2.direction = "left"
        self.add_image(path="images/water.png")


class Explosion(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/explosion.png")


class Robot(Actor):
    def __init__(self, position):
        super().__init__(position)
        self.costume.orientation = - 90

    def act(self):
        self.move()
        other = self.sensing_token(distance=0, token_type=Robot)
        if other:
            explosion = Explosion()
            self.board.add_to_board(explosion, position=self.position)
            self.remove()
            other.remove()


board = MyBoard()
board.show()
