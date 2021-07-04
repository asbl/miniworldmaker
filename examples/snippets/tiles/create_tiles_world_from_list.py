import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns=5
board.rows=5
board.tile_size=40
board.add_background("images/soccer_green.jpg")
board.speed = 1
stones = []
content = ["   *  ",
           " ***  ",
           "****  ",
           " **** ",
           "  ****"
           ]

for i in range(len(content)):
    for j in range(len(content[0])):
        print(i,j, content[i][j])
        if content[i][j] == '*':
            stone = miniworldmaker.Token(position=(i,j))
            stone.add_costume("images/stone.png")
            stones.append(stone)
            

board.run()
