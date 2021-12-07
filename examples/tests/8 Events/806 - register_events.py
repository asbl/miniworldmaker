import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background((0,0,0,100))
board.columns = 5
board.rows = 5
board.tile_size = 40

class MyToken(miniworldmaker.Token):
    def on_key_down(self, key):
        print(key)

    def on_key_down_a(self):
        print("a down")
        
    def on_setup(self):
        print ({name for name, thing in vars(self.__class__).items() if callable(thing)})
        pass
        #print(self.board.event_handler.registered_events)
        #print(self.board.event_handler.registered_events["on_key_down"])
        #print(self.board.event_handler.registered_events["on_key_pressed"])
my_token = MyToken()
board.run()



