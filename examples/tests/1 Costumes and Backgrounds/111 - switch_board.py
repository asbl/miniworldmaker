import miniworldmaker

class Board1(miniworldmaker.PixelBoard):
    def on_setup(self):
        self.add_background((0,255,0,255))
        print("board 1 was created")
        token = miniworldmaker.Token((10,10))
        
    def act(self):
        print("board 1 is running", self.frame)
        if self.frame == 20:
            board2 = Board2((400, 600))
            self.switch_board(board2)
            
    
class Board2(miniworldmaker.PixelBoard):
    def on_setup(self):
        self.add_background((0,0,100,255))
        token = miniworldmaker.Token((40,40))
        print("board 2 was created")
        
    def act(self):
        print("board 2 is running")
        
        
        
board = Board1(400,600)
#miniworldmaker.ActionTimer(20,board.switch_board, Board2())
board.run()