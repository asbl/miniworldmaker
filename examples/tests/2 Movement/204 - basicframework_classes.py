import miniworldmaker as mwm

class MyBoard(mwm.TiledBoard):

    def on_setup(self):
        print("setup board")
        self.rounds = 1
        self.counter = mwm.NumberToken(position=(4, 3), number=self.rounds)
        Player(position=(3, 3))
        self.add_background("images/stone.png")
        self.background.is_scaled_to_tile = True
        self.background.is_textured = True
        self.background.grid_overlay = True
        self.speed = 30
        


class Player(mwm.Token):

    def on_setup(self):
        print("Setup player")
        self.add_costume("images/char_blue.png")
        self.costume.orientation = - 90

    def act(self):
        if not self.sensing_on_board(distance=1):
            self.turn_left(90)
        if self.position == (0, 0):
            self.board.rounds += 1
            self.board.counter.set_number(self.board.rounds)
        self.move()
        print (self.position)


def main():
    board = MyBoard(columns=20, rows=8, tile_size=42, tile_margin=0)
    board.run()


if __name__ == '__main__':
    main()
