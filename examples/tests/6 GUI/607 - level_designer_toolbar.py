import miniworldmaker
class LevelDesignerBoard(miniworldmaker.PixelBoard):
    def on_setup(self):
        self.size = (600,400)
        self.add_background((200,200,0,255))
        self.toolbar = self.add_container(miniworldmaker.LevelDesignerToolbar(board,[MyToken, Wall]), "right")
        print(self.app.container_manager.containers)

        
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



