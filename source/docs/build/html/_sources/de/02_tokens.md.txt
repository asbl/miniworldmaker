Tokens
=======

Ein Token ist ein Spielstein auf deinem Spielbrett. 

Alle Objekte in deiner Miniworld sind Tokens, die auf dem Spielbrett bewegt werden können.

## Ein Token erstellen

Nachdem du das Spielbrett erstellt hast, wird nun ein Token, *(d.h. eine Spielfigur)* auf dem Board platziert.

Dies geht so:

```{code-block} python
---
lineno-start: 1
emphasize-lines: 9,10
---
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_background("images/soccer_green.jpg")
board.speed = 30
player = miniworldmaker.Token()
player.add_costume("images/player.png")

board.run()
```

  * In Zeile 9 wird ein Player-Objekt erstellt.
  
  * In Zeile 10 wird dem Player-Objekt ein Küstüm zugewiesen. 

### Das Kostüm

Jedes `Board` hat einen `Background`, jedes `Token` hat ein `Costume`. Du **musst* einem neuen Token ein Kostüm zuweisen. 

Die Anweisung dafür lautet üblicherweise:
```
token_name.add_costume("path_to_image")
```

![tiles](../images/add_costume.jpg)

`path_to_image` ist ein (relativer Pfad) zum Bild. Du solltest deine Bilder in den Unterordner `images` ablgegen, dann hat das Bild `bild.png` in dem Unterordner `images` den Pfad `images/bild.png.

### Ergebnis

![tiles](../_images/token.jpg)

### Ausblick

--> Mehr Informationen. Siehe [Tokens](../key_concepts/tokens.md)
