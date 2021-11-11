import miniworldmaker

board = miniworldmaker.PhysicsBoard()
# Black board
board.add_background("images/backgroundColorGrass.png")
board.size = (400, 600)

token1 = miniworldmaker.Token(position=(200, 100), image="images/stone.png")
token1.size = (100,50)
token1.costume.is_textured = True


plattform = miniworldmaker.Token(position=(100, 300), image="images/stone.png")
plattform.size = (200,20)
plattform.direction = 0
plattform.costume.is_textured = True
plattform.physics.simulation = "manual"


board.run()
