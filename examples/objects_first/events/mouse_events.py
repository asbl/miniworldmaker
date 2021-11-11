import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background((255, 255, 255, 255))
board.columns = 5
board.rows = 5
board.tile_size = 40

@board.register
def on_mouse_left(self, position):
    print("left" + str(position))
    
@board.register
def on_mouse_right(self, position):
    print("right" + str(position))
    
@board.register
def on_mouse_middle(self, position):
    print("middle" + str(position))
    
@board.register
def on_mouse_motion(self, position):
    print("motion" + str(position))
    
board.run()

