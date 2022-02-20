********************************************
Zeichnen mit dem Miniworldmaker - Grundlagen
*********************************************

Hier lernst du das Programmieren mit dem miniworldmaker kennen. Der miniworldmaker hat einen *Processing*-Modus, der sich an der populären Grafikprogrammierumgebung orientiert.

## Wie zeichnet man auf einem PC?

Monitore bestehen aus einem Gitter kleinester Quadrate. Diese Quadrate sind so klein, dass sie für uns wie Punkte aussehen. Man nennt diese kleinsten Quadrate *Pixel*.

Die Pixel sind in einem *Koordinatensystem* angeordnet. Dieses ist allerdings leicht anders aufgebaut, denn in der Regel ist der Ursprung in der oberen linken Ecke:

![Coordinates](../_images/processing/coordinates.png)

### Wichtig

Informatiker zählen in der Regel beginnend mit 0, d.h. die obere linke Ecke hat die Koordinaten (0,0). Ist das Bildschirmfenster 800x600 groß, so hat die untere rechte Ecke die Koordinaten (799, 599)

## Das erste Programm

Ein miniworldmaker-Programm besteht aus mehreren Teilen:

```python
from miniworldmaker import *
board = PixelBoard(800,600)

# Your code here

board.run()
```

  - 1: Die miniworldmaker Bibliothek wird importiert
  - 2: Ein Spielfeld wird erstellt mit den Maßen (800, 600)
  - 6: Am Ende wird die mainloop gestartet, dies muss immer die letzte Zeile deines Programms sein.

Dazwischen findet sich ein *Kommentar* - Kommentare beginnen immer mit einer # und werden vom Computer ignoriert und sind für **Menschen** gemacht. Sie dienen dazu, Programmierern Hinweise zu geben, hier z.B. das an diese Stelle dein eigener Code kommt.

Dieser könnte z.B. so aussehen:

```
from miniworldmaker import *

board = PixelBoard(800, 600)

Point((10,10))

board.run()
```

An die Stelle (10, 10) wird ein Pixel gezeichnet.

![Pixel](images/processing/pixel.png)

## Zeichnen geometrischer Grundformen.

Als nächstes lernst du, geometrische Grundformen zu zeichnen.

### Linien

Die Syntax zum Zeichnen einer Linie sieht folgendermaßen aus:

```python
Line(startpoint, endpoint)
```

startpoint und endpoint sind jeweils Tupel, z.B. (1, 2) für x=1 und y=2.

Wenn du eine Linie von (10,10) zu (100, 200) zeichnen willst so musst du z.B. folgendes schreiben:

```python
from miniworldmaker import *

board = PixelBoard(800, 600)
Line((10,10), (100, 200))
board.run()
```

### Kreise

Kreise kannst du allgemein folgendermaßen erstellen:

```python
Line(position, radius)
```

Die Position ist der Mittelpunkt des Kreises.

Wenn du einen Kreis an der Stelle (400,300) mit Radius 20 erstellen willst, musst du folgendes schreiben:


```python
from miniworldmaker import *

board = PixelBoard(800, 600)
Circle((400,300), 20)
board.run()
```

### Rechteck

Ein Rechteck wird beschrieben durch Position, Breite und Höhe:

```python
Rectangle(position, width, height)
```

 position beschreibt normalerweise die obere linke Ecke des Rechtecks.

Willst du ein Rechteck an der Position (100, 100) mit Breite 20 und Höhe 100 zeichnen, so musst du folgendes schreiben:

```python
from miniworldmaker import *

board = PixelBoard(800, 600)
Rectangle((100, 100), 20, 100)
board.run()
```

![rectangle](images/processing/rectangle.png)

### Ellipse

Ellipsen werden im Prinzip wie Rechtecke beschrieben, d.h. die Ellipse wird dann so gezeichnet, dass sie genau in das Rechteck hineinpasst. `width` und `height` beziehen sich hier jeweils auf den Durchmesser der Ellipse

```python
Ellipse(position, width, height)
```

Willst du eine Ellipse an der Position (100, 100) mit Breite 20 und Höhe 100 zeichnen, so musst du folgendes schreiben:

```python
from miniworldmaker import *

board = PixelBoard(800, 600)
Rectangle((100, 100), 20, 100)
board.run()
```

### Rechteck und Ellipse in die Mitte verschieben.

Oft will man ein Rechteck oder eine Ellipse nicht an der oberen linken Position erstellen, sondern am Mittelpunkt. Es gibt mehrere Möglichkeiten, wie man dies erreichen kann, ohne die Position manuell auszurechnen.

#### 1. from_center

Mit der Klassenmethode from_center kannst du eine Ellipse am Zentrum erstellen.

```python
from miniworldmaker import *

board = PixelBoard(100, 200)
Ellipse.from_center((50, 100), 100, 200)
board.run()
```

![Ellipse from center](images/processing/from_center.png))