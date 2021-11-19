import miniworldmaker
board = miniworldmaker.PixelBoard(600,400)
board.add_background((0,0,0,255))
board.toolbar = board.add_container(miniworldmaker.ActionBar(board),
                                    "bottom")
tkn = miniworldmaker.Token()
tkn.position = (50,50)
tkn.add_costume((255,255,255,255))
tkn.size= (80, 80)

@tkn.register
def act(self):
    self.move_right()

board.run()


