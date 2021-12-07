import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns=5
board.rows=5
board.tile_size=40
board.add_background("images/soccer_green.jpg")
board.add_background("images/space.jpg")
board.speed = 30

player1 = miniworldmaker.Token(position=(3, 4))
player1.add_costume("images/char_blue.png")
player1.costume.orientation = - 90

@player1.register
def on_sensing_token(self, token):
    if token == player2:
      print("Am i sensing player2?" + str(token == player2))

player2 = miniworldmaker.Token(position=(3, 4))
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90


board.run()