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
        if not self.sensing_borders(self.speed):
            self.move()
            print("scratch style", self.direction)
            print("unit circle", self.direction_at_unit_circle,Token.dir_to_unit_circle(self.direction))
            print("scratch style", Token.unit_circle_to_dir(Token.dir_to_unit_circle(self.direction)))

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

board = MyBoard()
board.show()

