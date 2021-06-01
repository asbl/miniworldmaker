from miniworldmaker import *


class MyBoard(PixelBoard):

    def on_setup(self):
        self.add_image(path="images/grass/land_grass11.png")
        self.background.is_textured = True
        self.background.tile_size = 40
        self.background.blit("images/roads/road_asphalt03.png", position=(80,0), size=(80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position = (80,80), size = (80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position=(80, 160), size=(80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position=(80, 240), size=(80, 80))
        self.background.blit("images/roads/road_asphalt39.png", position=(80, 320), size=(80, 80))
        self.background.blit("images/roads/road_asphalt02.png", position=(160, 320), size=(80, 80))
        self.background.blit("images/roads/road_asphalt02.png", position=(240, 320), size=(80, 80))
        self.background.blit("images/roads/road_asphalt41.png", position=(320, 320), size=(80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position=(320, 240), size=(80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position=(320, 160), size=(80, 80))
        self.background.blit("images/roads/road_asphalt01.png", position=(320, 80), size=(80, 80))
        self.background.blit("images/roads/road_asphalt05.png", position=(320, 00), size=(80, 80))
        self.background.blit("images/roads/road_asphalt02.png", position=(240, 00), size=(80, 80))
        self.background.blit("images/roads/road_asphalt02.png", position=(160, 00), size=(80, 80))
        self.background.is_scaled_to_tile = True
        self.player = Player(position = (100,60))
        self.colors = [(238, 238, 238, 255),
                       (232, 106, 23, 255),
                       (219, 98, 18, 255),
                       (250, 250, 250, 255)]

    def get_event(self, event, data):
        if event == "mouse_left":
            position = BoardPosition.from_pixel(data)

class Player(Token):

    def on_setup(self):
        self.add_image(path="images/motorcycles/motorcycle_green.png")
        self.costume.orientation = 0
        self.size=(40,40)
        self.turn_left(180)

    def on_key_pressed(self, keys):
            if "A" in keys:
                self.turn_left(10)
            if "D" in keys:
                self.turn_right(10)
            if "W" in keys:
                self.move()
                sensing_colors = self.sensing_colors(distance = 1, colors = self.board.colors)
                if (sensing_colors) or (not self.sensing_on_board()):
                    self.move_back()
            if "S" in keys:
                self.move(-1)
                sensing_colors = self.sensing_colors(distance = 1, colors = self.board.colors)
                intersections = [value for value in sensing_colors if value in self.board.colors]
                if intersections  or not self.sensing_on_board():
                    self.move(1)

    def on_mouse_left(self, pos):
        print(pos)


board = MyBoard(600, 400)
board.show()