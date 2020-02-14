import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background(path="images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_costume(path="images/player_1.png")
player.direction = 90
@player.register
def act(self):
    self.move()

@player.register
def act(self):
    self.move()
@player.register
def on_clicked_left(self, position):
    self.move_to((3,2))
board.run()