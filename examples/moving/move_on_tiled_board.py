from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(columns=20, rows=8, tile_size=42, tile_margin=1)
        player1 = Player()
        player = self.add_to_board(player1, position=(1, 1))
        print(player.image.get_rect())
        print(player.size)
        self.add_image(path="images/soccer_green.jpg")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(path="images/char_blue.png")
        self.set_upscale()

    def act(self):
        if self.is_looking_on_board():
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


board = MyBoard()
board.speed = 50
board.show()
