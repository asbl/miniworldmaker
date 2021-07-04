import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)
board.add_background("images/stone.jpg")

class MyToken(miniworldmaker.Token):
    def setup(self):
        self.add_costume("images/player.png")

my_token = MyToken()

board.run()