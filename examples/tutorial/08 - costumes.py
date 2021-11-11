import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player1 = miniworldmaker.Token((2,6))
player1.add_costume(["images/1.png", "images/2.png", "images/3.png"])
player1.animate()

player2 = miniworldmaker.Token((3,6))
player2.add_costume(["images/1.png", "images/2.png", "images/3.png"])
player2.loop_animation(30)

board.run()




