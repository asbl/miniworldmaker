from miniworldmaker import *


class MyBoard(TiledBoard):
    def __init__(self):
        super().__init__(tile_size=40, columns=29, rows=1, tile_margin=0)
        robot1 = Robot()
        robot1.add_image("images/robo_green.png")
        self.add_to_board(robot1, board_position=(0, 0))
        robot2 = Robot()
        robot2.add
        robot2.add_image("images/robo_yellow.png")
        robot2.turn_left(180)
        self.add_to_board(robot2, board_position=(28, 0))
        self.add_image(path="images/water.png")

    def act(self):
        pass

    def get_event(self, event, data):
        if event == "collision":
            for robot in data:
                robot.remove()
            explosion = Explosion()
            self.add_to_board(explosion, board_position=data[0].position)


class Explosion(Token):
    def __init__(self):
        super().__init__()
        self.add_image("images/explosion.png")


class Robot(Actor):
    def __init__(self):
        super().__init__()

    def act(self):
        self.move()

board = MyBoard()
board.speed = 50
board.show()
