import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)
board.add_background("images/stone")

class MyToken(miniworldmaker.Token):
    def setup(self):
        self.add_costume("images/player")
        self.add_costume("images/player.gif")

my_token = MyToken()

board.run()