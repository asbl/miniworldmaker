The Board
=============

Here we go!

## A first world

Wir erstellen eine erste Welt. Diese kann mit folgendem Code erzeugt werden:

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

  * In Zeile 1: Die miniworldmaker library wird importiert.
  * In Zeile 3: Ein neues `object` vom Typ `TiledBoard` wird erzeugt
  * In Zeile 4: Das neue Objekt erhält einen `background`.
  * In Zeile 5-8: Es werden verschiedene Attribute von 'board' verändert.
  * In Zeile 10: Das Spiel wird gestartet. Mit `board.run()` wird eine mainloop gestartet, die das Board immer und immer wieder neu zeichnet.

### Ergebnis:

Je nach Hintergrundbild sieht dein Ergebnis so aus:

![tiles](../_images/first.jpg)

### Variante: Show the grid

Du kannst auch das Grid anzeigen:

```
board.background.grid_overlay = True
```

### Ausblick: Verschiedene boards

Es gibt mehrere Kind-Klassen von Board

  * Ein `PixelBoard` ist für pixelgenaue Darstellungen vorgesehen
  
  * Ein `TiledBoard` ist geeignet für Boards, bei denen sich die Akteure auf "Kacheln" bewegen.
  

Einige Features der Boards (z.B. Kollissionen) unterscheiden sich geringfügig.

> Mehr Informationen, siehe [Key-Concept: Boards](../key_concepts/boards.md)

### Examples

> [Basic Framework](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/basics/basicframework_objects.py) - Ein erstes Programm, mit dem du starten kannst.

> [Basic Framework - With Classes](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/basics/basicframework_classes.py) - Wenn du bereits OOP Klassen kennst, kannst du mit diesem Framework starten.