from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_image(path="images/stone.jpg")
        Robot(position=(50, 50))


class Robot(Actor):

    def on_setup(self):
        self.size = (30, 30)
        self.add_image("images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        pass

    def on_key_pressed(self, keys):
        if "A" in keys:
            self.turn_left(10)
        if "D" in keys:
            self.turn_right(10)
        if "W" in keys:
            self.move()
            if not self.sensing_on_board(self.speed):
                self.move_back()

    def on_mouse_left(self, mouse_pos):
        print(mouse_pos)

board = MyBoard(800, 600)
board.show()
