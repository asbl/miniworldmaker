from miniworldmaker import *


class MyBoard(TiledBoard):

    def on_setup(self):
        self.tile_size = 30
        robo1 = Robot(position=(1, 1))
        # Draw border
        for i in range(self.rows):
            self.add_to_board(Wall(), position=(0, i))
        for i in range(self.rows):
            self.add_to_board(Wall(), position=(self.rows - 1, i))
        for i in range(self.columns):
            self.add_to_board(Wall(), position=(i, 0))
        for i in range(self.columns - 1):
            self.add_to_board(Wall(), position=(i, self.columns - 1))
        self.add_image(path="images/stone.jpg")


class Robot(Actor):

    def on_setup(self):
        self.add_image(path="images/robo_green.png")
        self.costume.orientation = - 90

    def act(self):
        actors = self.sensing_tokens(token_type=Wall)
        if not actors:
            self.move()
        else:
            self.turn_right(90)


class Wall(Token):

    def on_setup(self):
        self.add_image("images/rock.png")


board = MyBoard(20, 20)
board.show()
