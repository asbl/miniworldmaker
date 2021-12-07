import miniworldmaker

board = miniworldmaker.PixelBoard()
board.columns=300
board.rows=200
board.add_background("images/soccer_green.jpg")
board.add_background("images/space.jpg")

for i in range(1000):
    player1 = miniworldmaker.Token(position=(30, 4), static = False)
    player1.size = (40, 40)
    player1.add_costume("images/char_blue.png")
    player1.costume.orientation = - 90
    

board.run()