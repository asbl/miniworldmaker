from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=280, rows=100)
        self.add_image("images/water.png")
        player1 = Robot(position=(0, 0))
        self.speed = 1


class Robot(Actor):

    def on_setup(self):
        self.add_image("images/robo_green.png")
        self.costume.orientation = - 90
        self.costume.animation_speed = 30
        self.costume.is_animated = True
        self.animation1 = ["images/1.png", "images/2.png", "images/3.png", "images/4.png", "images/5.png"]
        self.size = (99, 99)
        self.direction = "right"
        self.i = 0
        self.timer = LoopActionTimer(180, self.costume.animate, ["animate!!!", self.animation1])
        print(self.costume.images_list)

    def act(self):
        if self.sensing_on_board():
            # self.move()
            pass
        pass

    def on_sensing_not_on_board(self):
        self.flip_x()
        self.move()


board = MyBoard()
board.run()
