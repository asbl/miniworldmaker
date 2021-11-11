import miniworldmaker

board = miniworldmaker.PixelBoard()
# Black board
board.add_background((0, 0, 0, 100))
board.columns = 3
board.rows = 8
board.tile_size = 40


# Token1 at position (2,1) with player costume
token1 = miniworldmaker.Token(position=(0, 1), image="images/player.png")
token1.costume.orientation = -90
print(token1.position)
print("default directiob", token1.direction)
print("default orientation", token1.costume.orientation)
token2 = miniworldmaker.Token(position=(0, 2), image="images/player.png")
token2.costume.orientation = 90
token3 = miniworldmaker.Token(position=(0, 3), image="images/player.png")
token3.costume.orientation = 180
token4 = miniworldmaker.Token(position=(0, 4), image="images/player.png")
token4.costume.orientation = 270