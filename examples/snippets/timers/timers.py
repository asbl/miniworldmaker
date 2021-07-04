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

miniworldmaker.ActionTimer(24, player.move, None)

miniworldmaker.LoopTimer(48, player.move, 2)

board.run()
