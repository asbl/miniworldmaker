from miniworldmaker import *

board = PixelBoard(columns=280, rows=100)
board.add_background("images/water.png")
board.speed = 1

robo = Token(position=(0, 0))
robo.add_costume()
robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
robo.size = (99, 99)
robo.loop_animation(120)
robo.costume.orientation = - 90
robo.costume.animation_speed = 20
robo.direction = "right"
@robo.register
def act(self):
    if self.sensing_on_board():
        self.move()
@robo.register
def on_sensing_not_on_board(self):
    self.flip_x()
    self.move()

board.run()

