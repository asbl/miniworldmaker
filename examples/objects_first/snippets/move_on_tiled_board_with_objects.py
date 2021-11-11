import miniworldmaker

board = miniworldmaker.TiledBoard()
board.tile_size = 60
board.add_background("images/soccer_green.jpg")
board.background.is_scaled = True
board.speed = 10

player = miniworldmaker.Token()
player.add_costume("images/char_blue.png")
player.costume.is_upscaled = True
player.costume.orientation = - 90
@player.register
def act(self):
    if self.sensing_on_board(1):
        self.move()
@player.register
def on_key_down_w(self):
    self.direction = "up"
@player.register
def on_key_down_s(self):
    self.direction = "down"
@player.register
def on_key_down_a(self):
    self.direction = "left"
@player.register
def on_key_down_d(self):
    self.direction = "right"

board.run()
