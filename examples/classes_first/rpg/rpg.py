import miniworldmaker

class MyBoard(miniworldmaker.TiledBoard):

    def on_setup(self):
        self.columns = 24
        self.rows = 14
        self.tile_size = 20
        self.add_background((255,255,255,0))
        for i in range(self.rows):
            for j in range(self.columns):
                Grass((j, i))
        Wall((0, 4))
        Wall((1, 4))
        Wall((2, 4))
        Wall((3, 4))
        Wall((4, 4))
        Wall((5, 4))
        Wall((6, 4))
        Wall((6, 0))
        Wall((6, 1))
        Wall((6, 3))
        self.torch = Torch((10, 4))
        self.fireplace = Fireplace((10, 12))
        self.door = Door((6, 2))
        self.player = Player((8, 2))
        self.play_music("rpgsounds/bensound-betterdays.mp3")
        self.toolbar = self.add_container(miniworldmaker.Toolbar(), "right", size = 200)
        self.console = self.add_container(miniworldmaker.Console(), "bottom", size = 100)

    def on_message(self, data):
        if data == "Fackel":
            fireplace = self.player.sensing_token(Fireplace)
            if fireplace:
                self.console.newline("Du zündest die Feuerstelle an.")
                self.fireplace.burn()
                self.toolbar.remove_widget("Fackel")


class Player(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/knight.png")
        self.costume.is_rotatable = False
        self.inventory = []

    def on_key_down_w(self):
        self.move_up()

    def on_key_down_s(self):
        self.move_down()

    def on_key_down_a(self):
        self.move_left()

    def on_key_down_d(self):
        self.move_right()

    def on_sensing_torch(self, torch):
        reply = self.ask.choices("Du findest eine Fackel. Möchtest du sie aufheben?",["Ja", "Nein"])
        if reply == "Ja":
            self.inventory.append("Torch")
            self.board.torch.remove()
            self.board.console.newline("Du hebst die Fackel auf.")
        self.board.toolbar.add_widget(miniworldmaker.ToolbarButton("Fackel", "rpgimages/torch.png"))

    def on_sensing_wall(self, wall):
        self.move_back()

    def on_sensing_door(self, door):
        if door.closed:
            self.move_back()           
            message = "Die Tür ist geschlossen... möchtest du sie öffnen"
            reply = self.ask.choices(message, ["Ja", "Nein"])
            if reply == "Ja":
                self.board.door.open()
                self.board.console.newline("Du hast das Tor geöffnet.")
        else:
            self.board.console.newline("Du gehst durch das Tor...")

class Wall(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/wall.png")
        self.static = True


class Grass(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/grass.png")
        self.static = True

class Torch(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/torch.png")


class Fireplace(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/fireplace_0.png")
        self.costume_burned = self.add_costume(["rpgimages/fireplace_1.png", "rpgimages/fireplace_2.png"])
        self.burning = False

    def burn(self):
        if self.burning == False:
            self.board.play_sound("rpgsounds/fireplace.wav")
            self.switch_costume(self.costume_burned)
            self.costume.is_animated = True


class Door(miniworldmaker.Token):

    def on_setup(self):
        self.add_costume("rpgimages/door_closed.png")
        self.costume_open = self.add_costume("rpgimages/door_open.png")
        self.closed = True

    def open(self):
        if self.closed == True:
            self.switch_costume(self.costume_open)
            self.board.play_sound("rpgsounds/olddoor.wav")
            self.closed = False


myboard = MyBoard()
myboard.run()
