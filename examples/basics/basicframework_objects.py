import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns=20
board.rows=8
board.tile_size=40
board.add_background("images/soccer_green.jpg")
board.add_background("images/space.jpg")
board.speed = 30

player = miniworldmaker.Token(position=(3, 4))
player.add_costume("images/char_blue.png")
player.costume.orientation = - 90

@player.register
def on_key_down(self, data):
    if "A" in data:
        self.turn_left()
    if "D" in data:
        self.turn_right()
    if "X" in data:
        self.board.switch_background()
    if not self.sensing_on_board(distance=0):
        self.move(-1)

@player.register
def act(self):
        if self.sensing_on_board(distance=1):
            self.move()

board.run()
