import miniworldmaker
board = miniworldmaker.TiledBoard()
board.add_background((255, 255, 255, 255))
board.columns = 5
board.rows = 5
board.tile_size = 40
token = miniworldmaker.Token((2,2))

@token.register
def on_clicked_left(self, position):
    print("clicked" + str(position))
    
@token.register
def on_mouse_leave(self, position):
    print("leave" + str(position))
    
board.run()