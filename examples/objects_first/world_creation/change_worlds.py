import miniworldmaker

board = miniworldmaker.TiledBoard()

board.columns = 5
board.rows = 5
board.tile_size = 40

board.add_background("images/soccer_green.jpg")

board.speed = 1
stones = []
world1 = ["  *  ",
          "***  ",
          "***  ",
          "**** ",
          " ****"
           ]

world2 = ["   * ",
          "*    ",
          "*    ",
          "*    ",
          "*    "
           ]

world3 = list()

def create_world(content):
    for i in range(len(content)): # outer array, i is column
        for j in range(len(content[0])): # row string, j is row
            if content[i][j] == '*':
                stone = miniworldmaker.Token()
                stone.position = (j, i)
                stone.add_costume("images/stone.png")
                stones.append(stone)

create_world(world1)

def save_world():
    world=[]
    for i in range(board.rows):
        row = ""
        for j in range(board.columns):
            if board.sensing_tokens(position=(j, i)):
                row += "*"
            else:
                row += " "
        world.append(row)
    return world

current_world = 1
    
@board.register
def on_key_down(self, data):
    global world1
    global world2
    global world3
    global current_world
    self.stop()
    print("World 1")
    print(world1)
    print("World 2")
    print(world2)
    print("World 3")
    print(world3)
    print("Actual World")
    print(save_world())
    if "SPACE" in data:
        if current_world == 1:
            world1 = save_world()
            self.clean()
            create_world(world2)
            current_world = 2
        elif current_world == 2:
            world2 = save_world()
            self.clean()
            create_world(world1)
            current_world = 1
    if "X" in data:
        self.clean()
    if "S" in data:
        world3 = save_world()
    self.start()
    
board.run()