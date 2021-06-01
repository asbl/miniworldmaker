import miniworldmaker


class MyBoard(miniworldmaker.TiledBoard):

    def on_setup(self):
        self.add_image(path="images/soccer_green.jpg")
        self.player = Player(position=(3, 4))
        self.speed = 30
        stone = self.add_background(("images/stone.png"))
        stone.is_textured = True
        stone.is_scaled_to_tile = True
        
    def on_key_down(self, data):
        print(data)
        if "A" in data:
            print("A")


class Player(miniworldmaker.Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image(path="images/char_blue.png")
        self.costume.orientation = - 90

    def on_key_down(self, data):
        if "A" in data:
            self.turn_left()
        if "D" in data:
            self.turn_right()
            print("D")
        if "W" in data:
            if self.sensing_on_board(distance=1):
                self.move()
        if "X" in data:
            self.board.switch_background()
        if not self.sensing_on_board(distance=0):
            self.move(-1)

    def act(self):
        if self.sensing_on_board(distance=1):
            self.move()


def main():
    board = MyBoard(columns=20, rows=8, tile_size=42)
    board.run()


if __name__ == '__main__':
    main()
