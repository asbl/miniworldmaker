Das Spielfeld
=============

Los geht es!

## Eine erste Welt

Wir erschaffen die erste Welt. Dies geht mit folgendem Code:

```{code-block} python
---
lineno-start: 1
emphasize-lines: 1,3,4,10
---
import miniworldmaker

board = miniworldmaker.TiledBoard()
board.add_background("images/soccer_green.jpg")
board.columns = 20
board.rows = 8
board.tile_size = 42
board.speed = 30

board.run()
```

### Was passiert hier?

  * In Zeile 1 wird die miniworldmaker-Bibliothek importiert.
  * In Zeile 3 wird ein neues `Objekt` von Typ `TiledBoard` erstellt.
  * In Zeile 4 erhält das neue erstellte Board-Objekt einen `Background`.
  * In Zeile 5-8 werden die verschiedenen Attribute des Objekts verändert.
  * In Zeile 10 wird das Spiel gestartet. Mir `board.run()` wird eine Mainloop gestartet, die das Board immer wieder neu zeichnet.

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

  * Ein `PixelBoard` ist für Pixelgenaue Darstellung von Inhalten gedacht.
  
  * Ein `TiledBoard` ist für Boards gedacht, bei denen sich die Akteure auf quadratischen Kacheln bewegen.
  

Die meisten der Funktionen unterscheiden sich nur geringfügig, da beide Boards Unterklassen der Klasse `Board` sind.

> Mehr Informationen. Siehe [Key-Concept: Boards](../key_concepts/boards.md)

### Beispiele

> [Basic Framework](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/basics/basicframework_objects.py) - Ein erstes Framework mit dem du anfangen kannst.

> [Basic Framework - Mit Klassen](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/basics/basicframework_classes.py) - Wenn du bereits Objektorientierung mit Klassen beherschst, dann kannst du acuh mit diesem Framework anfangen. Hier werden Klassen definiert, aus denen dann Objekte instanziiert werden.