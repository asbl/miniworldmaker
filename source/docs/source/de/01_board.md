Das Spielfeld
=============

Los geht es!

### Eine erste Welt

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

Zunächst wird eine eigene *Klasse* **MyBoard** erstellt. Diese ist eine Kindklasse von TiledBoard (*Gekacheltes Spielfeld*)
und erlaubt es dir, alle möglichen Spiele zu bauen, die auf Tiles(*Kacheln*) basieren.

  * Zeile 1: Mit der **import** Anweisung wird die Bibliothek miniworldmaker importiert.
  
  * Zeile 3: Das eigene Spielfeld wird als Kindklasse der Klasse Tiledboard definiert.
    
  * Zeile 5-6: Die on_setup() - Methode beim Objekt board *registriert*. Diese Methode wird aufgerufe, sobald das Board erstellt wird. Innerhalb der Methode werden einige Eigenschaften des Spielfeldes definiert: 
  
    * Anzahl Zeilen und Spalten (Zeile 7-8)
    
    * Größe einer einzelnen Kachel (Zeile 9)
    
    * Der Bildschirmhintergrund (Zeile 10) 

### Starten der Mainloop

Dies ist immer der letzte Befehl in deinem Programm:

```
board.run()
```

Die Mainloop wird gestartet, d.h. jetzt wird immer wieder der Bildschirm neu gezeichnet, auf Ereignisse reagiert, ...

### Ergebnis:

Je nach Hintergrundbild sieht das Ergebnis bei dir so aus:

![tiles](../_images/first.jpg)

### Das Grid anzeigen

Wenn du möchtest kannst du dir auch die Grenzen der einzelnen Tiles anzeigen lassen.
Ändere dazu die Methode setup() in der Klasse MyBoard ab:

```
    def setup()
        ...
        self.background.grid_overlay = True
```



### Verschiedene Boards

Es gibt verschiedene Unterklassen der Klasse Board:

  * Ein PixelGrid ist für Pixelgenaue Darstellung von Inhalten gedacht.
  
  * Ein TiledBoard ist für Boards gedacht, bei denen sich die Akteure auf quadratischen Kacheln bewegen.
  
Die meisten der Funktionen unterscheiden sich nur geringfügig, da beide Boards Unterklassen der Klasse **Boards** sind.

