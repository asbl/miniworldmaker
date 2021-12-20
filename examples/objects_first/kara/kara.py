import karalib

karaboard = karalib.KaraBoard()

@karaboard.register    
def on_started(self):
    self.kara.move_right()
    self.kara.move_right()
    self.kara.move_left()
    self.kara.move_up()
    self.kara.move_up()
    self.kara.move_down()
    self.kara.move_left()
    self.kara.move_left()
    self.kara.move_right()
    self.kara.move_down()
    self.kara.move_down()
    


karaboard.run()

    
    
