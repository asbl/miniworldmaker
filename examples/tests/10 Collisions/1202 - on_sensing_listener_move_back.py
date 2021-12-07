import miniworldmaker
# Is player 1 sensing player 2? Should return True
board = miniworldmaker.TiledBoard()
board.columns=5
board.rows=5
board.tile_size=40
board.add_background("images/soccer_green.jpg")
board.add_background("images/space.jpg")
board.speed = 30

player1 = miniworldmaker.Token(position=(0, 2))
player1.add_costume("images/char_blue.png")
player1.costume.orientation = - 90

player2 = miniworldmaker.Token(position=(3, 2))
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90

@player1.register
def act(self):
    global player2
    print("---------------act-----------------")
    print(self.position)
    self.move_right()
    print(self.position)
    if self.sensing_token(player2, distance = 0):
        print(self.position)
        self.move_back()
        print(self.position)
    
    
        
board.run()