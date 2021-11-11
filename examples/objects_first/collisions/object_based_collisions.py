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

player2 = miniworldmaker.Token(position=(3, 4))
player2.add_costume("images/char_blue.png")
player2.costume.orientation = - 90

player3 = miniworldmaker.Token(position=(6, 2))
player3.add_costume("images/char_blue.png")
player3.costume.orientation = - 90

player4 = miniworldmaker.Token(position=(0, 0))
player4.add_costume("images/char_blue.png")
player4.costume.orientation = - 90

@player1.register
def on_sensing_token(self, token):
    print("Player 1: Sensing token:")
    if token == player2:
      print("Am i sensing player2?" + str(token == player2))
      
@player3.register
def on_sensing_not_on_board(self):
  print("Player 3: Sensing on board:")
  print("Warning: I'm not on the board!!!")
  
@player4.register
def on_sensing_borders(self, borders):
  print("Player 4: Sensing borders:")
  print("Borders are here!", str(borders))
    
board.run()