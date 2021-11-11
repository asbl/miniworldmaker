import miniworldmaker

board = miniworldmaker.TiledBoard()
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
token5 = miniworldmaker.Token(position=(1, 2), image="images/player.png")
token5.costume.orientation = 90
token5.direction = 90
# Unit circle
token6 = miniworldmaker.Token(position=(2, 1), image="images/player.png")
token6.costume.orientation = -90
token6.direction_at_unit_circle = 0
token7 = miniworldmaker.Token(position=(2, 2), image="images/player.png")
token7.costume.orientation = -90
token7.direction_at_unit_circle = 90
token8 = miniworldmaker.Token(position=(2, 3), image="images/player.png")
token8.costume.orientation = -90
token8.direction_at_unit_circle = 180
token9 = miniworldmaker.Token(position=(2, 4), image="images/player.png")
token9.costume.orientation = -90
token9.direction_at_unit_circle = 270

board.run()