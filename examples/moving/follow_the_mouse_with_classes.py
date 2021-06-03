from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_background("images/stone.jpg")
        Robot(position=(50, 50))


class Robot(Token):

    def on_setup(self):
        self.size = (30, 30)
        self.add_costume("images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        mouse = self.board.get_mouse_position()
        if mouse:
            self.point_towards_position(mouse)
            self.move()


board = MyBoard(800, 600)
board.run()
