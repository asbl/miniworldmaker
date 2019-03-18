from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=400, rows=400)
        robo1 = self.add_actor(Robot(), (20, 20))
        self.add_image("images/stone.jpg")


class Robot(Actor):
    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")
        self.size=(30, 30)

    def act(self):
        self.move(distance=3)

    def get_event(self, event, data):
        if event == "key":
            if "W" in data:
                self.turn_left(10)
            elif "S" in data:
                self.turn_right(10)


board = MyBoard()
board.speed = 60
board.show_log()
board.show()
