from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=400, rows=200)
        self.add_image(path="images/stone.jpg")
        Robot(position=(50, 50))


class Robot(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.size = (30, 30)
        self.add_image("images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        if not self.sensing_on_board():
            self.turn_left(270)

    def get_event(self, event, data):
        if event == "key_pressed":
            if "A" in data:
                self.turn_left(10)
            if "D" in data:
                self.turn_right(10)
            if "W" in data:
                self.move()


board = MyBoard()
board.show()
