from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=200, rows=200)
        player1 = Player()
        self.add_to_board(player1, position=(30, 30))
        self.add_image("images/soccer_green.jpg")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image("images/robo_green.png")

    def act(self):
        self.move()

    def get_event(self, event, data):
        if event == "key":
            if "W" in data:
                self.move(direction="up")
            elif "S" in data:
                self.move(direction="down")
            elif "A" in data:
                self.move(direction="left")
            elif "D" in data:
                self.move(direction="right")


board = MyBoard()
board.show()
