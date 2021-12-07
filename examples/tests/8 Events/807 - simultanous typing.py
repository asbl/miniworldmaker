import miniworldmaker
board = miniworldmaker.TiledBoard(4,4)
player1 = miniworldmaker.Token(position=(0, 2))
player2 = miniworldmaker.Token(position=(3, 2))


@player1.register
def on_key_down_a(self):
    print("player 1", self.board.frame)
        
@player2.register
def on_key_down_b(self):
    print("player 2", self.board.frame)


board.run()