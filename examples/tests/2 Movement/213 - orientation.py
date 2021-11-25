import miniworldmaker
board = miniworldmaker.PixelBoard(200,200)

player1 = miniworldmaker.Token(position=(0, 0))
player1.size = (40, 40)
player1.add_costume("images/char_blue.png")
player1.costume.orientation = 0

player2 = miniworldmaker.Token(position=(40, 0))
player2.size = (40, 40)
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90

player3 = miniworldmaker.Token(position=(80, 0))
player3.size = (40, 40)
player3.add_costume("images/char_blue.png")
player3.costume.orientation = 180

player4 = miniworldmaker.Token(position=(120, 0))
player4.size = (40, 40)
player4.add_costume("images/char_blue.png")
player4.costume.orientation = 90

class Player5(miniworldmaker.Token):
    def on_setup(self):
        self.size = (40, 40)
        self.add_costume("images/char_blue.png")
        self.costume.orientation = 90
        
player5 = Player5(position = (160,0))

board.run()