import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background((0,0,0,100))
board.columns = 5
board.rows = 5
board.tile_size = 40

token1 = miniworldmaker.Token(position = (2, 2) )
token1.add_costume((100,0,100,100))

token2 = miniworldmaker.Token(position = (2, 2) )
token2.send_message("Hello from " + str(token2))


@token1.register
def on_message(self, message):
    print(str(self) + ":received message:" + message)

board.run()


