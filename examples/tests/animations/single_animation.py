from miniworldmaker import *

board = PixelBoard(columns=280, rows=100)
board.add_background("images/water.png")
board.speed = 1

robo = Token(position=(0, 0))
robo.add_costume()
robo.costume.add_images(["images/1.png"])
robo.costume.add_images(["images/2.png","images/3.png","images/4.png"])
robo.size = (99, 99)
robo.costume.animation_speed = 20
robo.costume.animate()
board.run()

