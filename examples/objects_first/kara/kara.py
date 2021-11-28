import karalib

karaboard = karalib.KaraBoard()

@karaboard.register    
def on_run(self):
    self.kara.move_right()
    self.kara.move_right()


karaboard.run()

    
    
