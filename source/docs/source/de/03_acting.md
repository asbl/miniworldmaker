Acting
======

Das Spielfeld und alle Tokens können über die Methode act() gesteuert werden. 
Diese Methode wird immer wieder aufgerufen (genau genommen: Alle board.speed Schritte).
In dieser Methode werden alle wiederkehrenden Handlungen von Tokens ausgeführt.

Wenn du ein Token erstellst, kannst du mit dem Decorator @register eine Act-Methode zum Spielfeld oder zum Token hinzufügen:

Beispiel:
```
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_image(path="images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_image(path="images/player_1.png")
player.direction = 90
@player.register
def act(self):
    self.move()

board.run()
```