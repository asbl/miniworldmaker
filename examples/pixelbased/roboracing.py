from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_image(path="images/stone.jpg")
        robot = Robot(position=(200, 200))
        wall = Wall(position = (100,100))


class Wall(Actor):

    def on_setup(self):
        self.add_image(path="images/wall.png")
        self.size= (64, 64)

class Robot(Actor):

    def on_setup(self):
        self.add_image("images/robo_green.png")
        self.costume.orientation = - 90
        self.size=(64,64)

    def act(self):
        pass

    def on_key_pressed(self, keys):
        print(self.position, self.center, self.image)
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

    def on_sensing_wall(self, wall):
        print(wall)
        self.move_back()

    def on_mouse_left(self, mouse_pos):
        print(mouse_pos)

board = MyBoard(800, 600)
board.show()
