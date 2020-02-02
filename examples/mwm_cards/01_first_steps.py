import miniworldmaker


def main():
    board = miniworldmaker.TiledBoard(columns=20, rows=8, background_image="images/soccer_green.jpg")
    player = miniworldmaker.Token(position=(3, 4), image="images/char_blue.png")
    player2 = miniworldmaker.Token(position=(6, 4), image="images/char_blue.png")
    player.costume.orientation = - 90
    player2.costume.orientation = - 90

    @player.register
    def on_key_down(self, keys):
        if "A" in keys:
            self.turn_left()
        if "D" in keys:
            self.turn_right()
        if "W" in keys:
            self.move()
        if not self.sensing_on_board(distance=0):
            self.move(-1)

    @player2.register
    def on_key_down_c(self):
        print("method called")
        self.turn_left()

    board.run()


if __name__ == '__main__':
    main()
