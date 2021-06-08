import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background("images/space.jpg")
board.columns=20
board.rows=8
board.tile_size=40
board.fps=60
board.run()
