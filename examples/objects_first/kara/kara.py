import karalib

karaboard = karalib.KaraBoard()

@karaboard.register    
def on_started(self):
    self.kara.move_right()
    self.kara.move_right()


karaboard.run()

    
    
