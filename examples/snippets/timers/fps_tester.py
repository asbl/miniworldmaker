import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns=20
board.rows=8
board.tile_size=40
board.add_background("images/space.jpg")
board.fps=60
player = miniworldmaker.Token(position=(3, 4))
player.add_costume("images/char_blue.png")
player.costume.orientation = - 90
@player.register
def act(self):
    print(board.frame)

def special_action():
    player.move()
    print("player moved at " + str(board.frame))
miniworldmaker.ActionTimer(24, special_action)
miniworldmaker.ActionTimer(48, special_action)

board.run()
