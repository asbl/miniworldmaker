import miniworldmaker

class MyBoard(miniworldmaker.TiledBoard):
    def on_setup(self):
        self.columns = 5
        self.rows = 5
        self.tile_size = 40
        self.add_background("images/soccer_green.jpg")
        token = miniworldmaker.Token()
        token.position = (3,4)
        token.add_costume("images/player.png")
        # Bilder von:
        # https://www.kenney.nl/assets
        
board = MyBoard(8, 6)
board.run()
