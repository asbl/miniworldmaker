import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background("images/soccer_green.jpg")
board.columns=20
board.rows=8
board.tile_size=40

player = miniworldmaker.Token(position=(3, 4))
player.add_costume("images/char_blue.png")
print(player.position)

board.run()