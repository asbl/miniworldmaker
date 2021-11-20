import miniworldmaker
class LevelDesignerBoard(miniworldmaker.TiledBoard):
    def on_setup(self):
        self.size = (18,13)
        self.add_background((200,200,0,255))
        self.toolbar = self.add_container(miniworldmaker.LevelDesignerToolbar(board,[MyToken, Wall]), "right")
        print(self.app.container_manager.containers)

        
class MyToken(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume((255,255,255,255))
        
class Wall(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/wall.png")


board = LevelDesignerBoard()

board.run()




