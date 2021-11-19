from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_background("images/stone.jpg")
        robot = Robot(position=(280, 280))
        wall = Wall(position = (100,100))
        wall2 = Wall(position = (0, 0), image="images/wall.png") 


class Wall(Token):

    def on_setup(self):
        self.add_costume("images/wall.png")
        self.size= (64, 64)

class Robot(Token):

    def on_setup(self):
        self.add_costume("images/robo_green.png")
        self.costume.orientation = -90
        self.size= (64 , 512)
        self.costume.is_scaled = True

    def act(self):
        pass

    def on_key_pressed(self, keys):
        if "A" in keys:
            self.turn_left(10)
        if "D" in keys:
            self.turn_right(10)
        if "W" in keys:
            self.move()
            print(self.direction)
            print(self.position)
            if not self.sensing_on_board(self.speed):
                self.move_back()
        #print("scratch style (self.direction)", self.direction)
        #print("unit circle style (dir to unit circle)", Token.dir_to_unit_circle(self.direction))
        #print("scratch style again (unit circle to dir)", Token.unit_circle_to_dir(Token.dir_to_unit_circle(self.direction)))

    def on_sensing_wall(self, wall):
        self.move_back()

    def on_mouse_left(self, mouse_pos):
        print(mouse_pos)

board = MyBoard(800, 600)
board.run()
