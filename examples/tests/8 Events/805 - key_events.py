import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background((0,0,0,100))
board.columns = 5
board.rows = 5
board.tile_size = 40

token1 = miniworldmaker.Token(position = (2, 2) )
token1.add_costume((100,0,100,100))

@token1.register
def on_key_down(self, key):
    """
    A doc coment
    """
    print("key_down", key)

@token1.register
def on_key_down_a(self):
    print("key_down_a")

@token1.register
def on_key_pressed(self, key):
    print("pressed", key)
    
@token1.register
def on_key_pressed_s(self):
    print("pressed s")

board.run()


