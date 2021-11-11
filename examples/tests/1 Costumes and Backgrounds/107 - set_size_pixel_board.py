import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)

board.add_background("images/stone.jpg")

obj1 = miniworldmaker.Token(position=(50, 50))
obj1.size = (80,80)
obj2 = miniworldmaker.Token(position=(140, 50))
obj2.size = (20,80)
obj3 = miniworldmaker.Token(position=(170, 50))
obj3.size = (20,20)

pl1 = miniworldmaker.Token(position=(50, 200), image="images/player")
pl1.size = (80, 80)

pl2 = miniworldmaker.Token(position=(140, 200), image="images/player")
pl2.size = (20, 80)

pl3 = miniworldmaker.Token(position=(170, 200), image="images/player")
pl3.size = (20, 20)

class Sizer(miniworldmaker.Token):
    def on_setup(self):
        self.size = (80,80)
        
pl4 = Sizer(position=(240, 200), image="images/player")

class Sizer2(miniworldmaker.Token):
    def on_setup(self):
        self.size = (30,30)
  
pl5 = Sizer2(position=(290, 200), image="images/player")


board.run()