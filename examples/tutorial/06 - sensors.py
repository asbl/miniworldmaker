import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.Token()
player1.add_costume("images/player_1.png")
player2 = miniworldmaker.Token((8, 0))
player2.add_costume("images/player_1.png")
@player1.register
def act(self):
    self.direction = 90
    if not self.sensing_tokens():
        self.move()
walls = []
player2 = miniworldmaker.Token()
wall = miniworldmaker.Token()
walls.append(wall)

@player1.register
def on_sensing_token(self, other_token):
    if other_token.token_type in walls:
        pass # tue etwas
board.run()