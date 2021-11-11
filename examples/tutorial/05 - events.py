import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_costume("images/player_1.png")
@player.register
def on_key_down_w(self):
    self.move()
@player.register
def on_key_down_a(self):
    self.turn_left()
@player.register
def on_key_down_d(self):
    self.turn_right()
@player.register
def on_key_down_s(self):
    self.move_back()
board.run()


