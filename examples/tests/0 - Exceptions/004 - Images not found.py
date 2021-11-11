import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_blue.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_costume("images/player.png")

board.run()