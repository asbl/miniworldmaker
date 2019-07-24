from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_image(path="images/stone.jpg")
        robot = Robot(position=(400, 400))
        robot.speed = 1


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
        print("scratch style (self.direction)", self.direction)
        print("unit circle style (dir to unit circle)", Token.dir_to_unit_circle(self.direction))
        print("scratch style again (unit circle to dir)", Token.unit_circle_to_dir(Token.dir_to_unit_circle(self.direction)))

    def on_mouse_left(self, mouse_pos):
        print(mouse_pos)

board = MyBoard(800, 600)
board.show()
