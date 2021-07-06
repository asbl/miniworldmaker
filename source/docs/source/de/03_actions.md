Aktionen 
==========

## Die act()-Methode

Das Spielfeld und alle Tokens können über die Methode `act()` gesteuert werden. 
Diese Methode wird immer wieder aufgerufen *(genau genommen: Alle `board.speed` Zeiteinheiten)* bis das Spiel beendet wird.

Wenn du ein Token erstellst, kannst du mit dem Decorator `@register` eine `act()`-Methode zum Spielfeld oder zu deinen Token hinzufügen:

### Beispiel:

```{code-block} python
---
lineno-start: 1
emphasize-lines: 12,13,14
---
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

### Was passiert hier?

Interessant sind hier die Zeilen 12-14: Hier wird die Methode act zum Objekt `player` hinzugefügt. Der Decorator `@player.register` bindet die Methode an das Objekt `player`

