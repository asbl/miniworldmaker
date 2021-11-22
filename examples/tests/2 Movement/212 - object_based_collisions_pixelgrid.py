import miniworldmaker

board = miniworldmaker.PixelBoard()
board.columns=300
board.rows=200
board.add_background("images/soccer_green.jpg")
board.add_background("images/space.jpg")
board.speed = 30

player1 = miniworldmaker.Token(position=(30, 4))
player1.size = (40, 40)
player1.add_costume("images/char_blue.png")
player1.costume.orientation = - 90

player2 = miniworldmaker.Token(position=(3, 4))
player2.size = (40, 40)
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90

player2 = miniworldmaker.Token(position=(90, 4))
player2.size = (40, 40)
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90

@player1.register
def act(self):
    print("p1 rect", self.rect)


@player2.register
def act(self):
    print("p2 rect", self.rect)

@player1.register
def on_sensing_token(self, token):
    print("player 1: I'm sensing a collision with", token)
    print("token is player 2?", token==player2)
    
board.run()