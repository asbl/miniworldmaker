Das Spielfeld
=============

Los geht es!

## Eine erste Welt

Wir erschaffen die erste Welt. Dies geht mit folgendem Code:

```
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.columns = 20
board.rows = 8
board.tile_size = 42
board.add_image(path="images/soccer_green.jpg")
board.speed = 30

board.run()
```

### Was passiert hier?

  * In Zeile 1 wird die miniworldmaker-Bibliothek importiert.
  * In Zeile 3 wird ein neues **Objekt** von Typ **TiledBoard** erstellt.
  * In Zeile 2-6 werden die verschiedenen Attribute des Objekts verändert.
  * In Zeile 10 wird das Spiel gestartet. Mir und() wird eine Mainloop gestartet, die das Board immer wieder neu zeichnet.

### Ergebnis:

Je nach Hintergrundbild sieht das Ergebnis bei dir so aus:

![tiles](../_images/first.jpg)

### Variante: Das Grid anzeigen

Wenn du möchtest kannst du dir auch die Grenzen der einzelnen Tiles anzeigen lassen.

```
board.background.grid_overlay = True
```

### Ausblick: Verschiedene Boards

Es gibt verschiedene Unterklassen der Klasse Board:

  * Ein **PixelBoard** ist für Pixelgenaue Darstellung von Inhalten gedacht.
  
  * Ein **TiledBoard** ist für Boards gedacht, bei denen sich die Akteure auf quadratischen Kacheln bewegen.
  

Die meisten der Funktionen unterscheiden sich nur geringfügig, da beide Boards Unterklassen der Klasse **Boards** sind.

> Mehr Informationen. Siehe [Key-Concept: Boards](../key_concepts/boards.md)
