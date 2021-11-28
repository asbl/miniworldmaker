import karalib

karaboard = karalib.KaraBoard()

@karaboard.register    
def on_run(self):
    self.kara.move_right(1)
    self.kara.move_right(1)


karaboard.run()

    
    
