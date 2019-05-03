from miniworldmaker import *


class MyBoard(PixelBoard):

    def __init__(self):
        super().__init__(columns=200, rows=200)
        player1 = Player(position=(30, 30))
        self.add_image("images/soccer_green.jpg")



class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image("images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        self.move()

    def get_event(self, event, data):
        if event == "key_pressed":
            if "W" in data:
                self.point_in_direction("up")
            elif "S" in data:
                self.point_in_direction("down")
            elif "A" in data:
                self.point_in_direction("left")
            elif "D" in data:
                self.point_in_direction("right")
            if self.sensing_on_board():
                self.move()


board = MyBoard()
board.show()

