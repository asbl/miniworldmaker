from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=4, rows=4, tile_size=42, tile_margin=1)
        self.player = Player(position=(1, 1))
        self.add_image(path="images/soccer_green.jpg")


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image(path="images/char_blue.png")
        self.costume.is_upscaled = True
        self.costume.orientation = - 90

    def act(self):
        if self.sensing_on_board(1):
            self.move()

    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.direction = "up"
            elif "S" in data:
                self.direction = "down"
            elif "A" in data:
                self.direction = "left"
            elif "D" in data:
                self.direction = "right"


def main():
    board = MyBoard()
    board.show()


import cProfile

pr = cProfile.Profile()
pr.enable()
main()
pr.disable()
pr.dump_stats("profilefile.profile")
