import miniworldmaker

board = miniworldmaker.TiledBoard()
# Black board
board.add_background((0, 0, 0, 100))
board.columns = 5
board.rows = 5
board.tile_size = 40

# Token1 at position (2,1) with player costume
token1 = miniworldmaker.Token(position=(2, 1), image="images/player.png")

# Token2 at position (3,1) with purple backgrund
token2 = miniworldmaker.Token(position = (3, 1) )
token2.add_costume((100,0,100,100))
try:
    token2.size = (1,1)
except Exception as e:
    print(e)
token2.positin = (40,40)
print(token2.x, token2.y)

board.run()