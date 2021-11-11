import miniworldmaker

board = miniworldmaker.PixelBoard()
# Black board
board.add_background((0, 0, 0, 100))
board.size = (400, 300)
# tokens looking:
# * up(dir 0, or:-90)
# * down(dir 0, or:90)
# * left(dir 0, or:180)
# * right(dir 0, or:270)

# Token1 at position (2,1) with player costume
token1 = miniworldmaker.Token(position=(0, 50), image="images/player.png")
token1.costume.orientation = -90
print(token1.position)
print("default direction", token1.direction)
print("default orientation", token1.costume.orientation)

token2 = miniworldmaker.Token(position=(0, 100), image="images/player.png")
token2.costume.orientation = 90
token3 = miniworldmaker.Token(position=(0, 150), image="images/player.png")
token3.costume.orientation = 180
token4 = miniworldmaker.Token(position=(0, 200), image="images/player.png")
token4.costume.orientation = 270

print("token 4 position", token4.position, token4.rect)
class UpToken(miniworldmaker.Token):
    def on_setup(self):
        self.direction = 0
        self.costume.orientation = -90

class LeftToken(miniworldmaker.Token):
    def on_setup(self):
        self.direction = -90
        self.costume.orientation = -90

class DownToken(miniworldmaker.Token):
    def on_setup(self):
        self.direction = 180
        self.costume.orientation = -90

class RightToken(miniworldmaker.Token):
    def on_setup(self):
        self.direction = 90
        self.costume.orientation = -90


r = RightToken(position=(50, 50), image="images/player.png")
l = LeftToken(position=(50, 100), image="images/player.png")
u = UpToken(position=(50, 150), image="images/player.png")
d = DownToken(position=(50, 200), image="images/player.png")

board.run()