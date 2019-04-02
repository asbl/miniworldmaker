from miniworldmaker import *


class MyBoard(TiledBoard):
    def __init__(self):
        super().__init__(tile_size=40, columns=29, rows=1, tile_margin=0)
        robot1 = Robot()
        robot1.add_image("images/robo_green.png")
        self.add_to_board(robot1, position=(0, 0))
        robot2 = Robot()
        robot2.add_image("images/robo_yellow.png")
        robot2.turn_left(180)
        self.add_to_board(robot2, position=(28, 0))
        self.add_image(path="images/water.png")


class Explosion(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/explosion.png")


class Robot(Actor):
    def __init__(self):
        super().__init__()

    def act(self):
        self.move()
        other = self.sensing_token(distance=0, token=Robot)
        if other:
            explosion = Explosion()
            self.board.add_to_board(explosion, position=self.position)
            self.remove()
            other.remove()


board = MyBoard()
board.speed = 50
board.show()
