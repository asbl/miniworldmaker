import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns=5
board.rows=5
board.tile_size=40
board.add_background("images/soccer_green.jpg")
board.speed = 1
stones = []
for i in range(5):
    if i % 2 == 0:
        stone = miniworldmaker.Token(position=(i,2))
        stone.add_costume("images/stone.png")
        stones.append(stone)
        
player1 = miniworldmaker.Token(position=(3, 4))
player1.add_costume("images/player.png")
player1.costume.orientation = - 90

@player1.register
def on_key_down(self, data):
    if "A" in data:
        self.direction = -90
        self.move()
    if "D" in data:
        self.direction = 90
        self.move()
    if "W" in data:
        self.direction = 0
        self.move()
    if "S" in data:
        self.direction = 180
        self.move()

    if not self.sensing_on_board(distance=0):
        self.move(-1)
        
@player1.register
def on_sensing_token(self, other):
    global stones
    if other in stones:
        self.move_back()
        
@player1.register
def on_sensing_token(self, other):
    global stones
    if other in stones:
        self.move_back()
        
@player1.register
def on_sensing_token(self, other):
    global stones
    if other in stones:
        self.move_back()


board.run()