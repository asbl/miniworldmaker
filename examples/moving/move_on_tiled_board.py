from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 60
        self.player = Player(position=(1, 1))
        self.add_image(path="images/soccer_green.jpg")
        self.background.is_scaled = True
        print(self.is_running)


class Player(Actor):

    def on_setup(self):
        self.add_image(path="images/char_blue.png")
        self.costume.is_upscaled = True
        self.costume.orientation = - 90

    def act(self):
        if self.sensing_on_board(1):
            self.move()
            print("move")
        print("act")

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


board = MyBoard(6, 4)
board.show()
