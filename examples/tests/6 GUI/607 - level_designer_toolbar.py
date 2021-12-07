import miniworldmaker
class LevelDesignerBoard(miniworldmaker.PixelBoard):
    def on_setup(self):
        self.file = "data.db"
        self.size = (600,400)
        self.add_background((200,200,0,255))
        self.toolbar = self.add_container(miniworldmaker.LevelDesignerToolbar(self,[MyToken, Wall], self.file), "right")

    def on_board_loaded(self):
        self.load_tokens_from_db(self.file, [MyToken, Wall])
        

        
class MyToken(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume((255,255,255,255))
        self.size = (40, 40)
        
class Wall(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/wall.png")
        self.size = (40, 40)


board = LevelDesignerBoard()

board.run()



