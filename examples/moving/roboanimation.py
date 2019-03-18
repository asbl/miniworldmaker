from miniworldmaker import *

class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=120, rows=75)
        self.add_image("images/water.png")
        player1 = Robot()
        self.add_actor(player1, position=(0, 0))


class Robot(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
        self.size = (75,75)
        self.animation_speed = 30
        self.animate()

    def act(self):
        if self.look_on_board(direction="forward"):
            self.move(direction = "forward")
        else:
            self.flip_x()


board = MyBoard()
board.show_log()
board.speed = 100
board.show()
