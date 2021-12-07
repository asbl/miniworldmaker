import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background((0,0,0,100))
board.columns = 5
board.rows = 5
board.tile_size = 40

@board.register
def on_mouse_left(self, position):
    print("left" + str(position), type(position))
    
@board.register
def on_mouse_right(self, position):
    print("right" + str(position))
    
@board.register
def on_mouse_middle(self, position):
    print("middle" + str(position))
    
@board.register
def on_mouse_motion(self, position):
    print("motion" + str(position))
  
token = miniworldmaker.Token(position = (2, 2) )
token.add_costume((100,0,100,100))

@token.register
def on_clicked_left(self, position):
    print("clicked left on token " + str(token))

board.run()

