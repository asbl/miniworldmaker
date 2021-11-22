import miniworldmaker
board = miniworldmaker.PixelBoard(200,200)

tkn = miniworldmaker.Token((0,0))
tkn.move_right(1)
tkn2 = miniworldmaker.Token((0,40))
tkn2.move_right(40)
tkn3 = miniworldmaker.Token((0,80))
tkn3.move_right(80)
board.run()