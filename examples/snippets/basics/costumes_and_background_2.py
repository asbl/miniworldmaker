import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)
board.add_background("images/stone.jpg")

robot = miniworldmaker.Token(position=(50, 50))

board.run()