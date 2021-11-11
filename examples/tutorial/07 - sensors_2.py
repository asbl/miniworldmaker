import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.Token((2,6))
player1.add_costume("images/player_1.png")
player2 = miniworldmaker.Token((5,3))
player2.add_costume("images/player_1.png")
player2.token_type = "actor"
walls = []
for i in range(5):
    wall = miniworldmaker.Token((i,i))
    wall.token_type = "wall"
    wall.add_costume("images/wall.png")
    walls.append(wall)

@player1.register
def on_sensing_token(self, other_token):
    if other_token.token_type == "actor":
        pass # tue etwa
    elif other_token.token_type == "wall":
        pass # tue etwas anders

@player1.register
def on_key_down_w(self):
    self.move_up()
@player1.register
def on_key_down_a(self):
    self.move_left()
@player1.register
def on_key_down_d(self):
    self.move_right()
@player1.register
def on_key_down_s(self):
    self.move_down()
    
@player1.register
def on_sensing_token(self, other):
    if other in walls:
        self.move_back()
board.run()



