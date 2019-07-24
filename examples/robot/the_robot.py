from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 30
        print("on setup", self.default_token_speed)
        robo1 = Robot(position=(1, 1))
        # Draw border
        for i in range(self.rows):
            Wall(position=(0, i))
        for i in range(self.rows):
            Wall(position=(self.rows - 1, i))
        for i in range(self.columns):
            Wall(position=(i, 0))
        for i in range(self.columns - 1):
            Wall(position=(i, self.columns - 1))
        self.add_image(path="images/stone.jpg")


class Robot(Actor):

    def on_setup(self):
        print("setup robot")
        self.add_image(path="images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        self.move()

    def on_sensing_wall(self, wall):
        self.move_back()
        self.turn_right(90)


class Wall(Token):

    def on_setup(self):
        self.add_image("images/rock.png")
        self.is_static = True


board = MyBoard(20, 20)
board.show()
