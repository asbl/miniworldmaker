# Farben und Konturen


## Einfärben


Eine geometrische Form kann mit dem Attribut ``fill_color`` eingefärbt werden:

```python
from miniworldmaker import *

board = PixelBoard(350, 150)
r = Rectangle((10,10), 100, 100)
r.fill_color = (255, 0, 0)

g = Rectangle((120,10), 100, 100)
g.fill_color = (0, 255,0)

b = Rectangle((230,10), 100, 100)
b.fill_color = (0, 0 ,255)

board.run()
```

Eine **Farbe** wird als 3-Tupel angegeben:

  * Der erste Wert ist der *rot*-Anteil

  * Der zweite Wert ist der *grün*-Anteil

  * Der dritte Wert ist der *blau*-Anteil

Durch "mischen" dieser Farben erhält man eine konkrete Farbe:

<img src="../_images/processing/rgb.png" alt="rgb colors" width="260px"/>

### Variablen

Wir haben hier *Variablen* verwendet. Bisher wenn wir ein Objekt angelegt haben, konnten wir darauf nicht mehr zugreifen. Hier haben wir den Rechtecken Namen gegeben (z.B. r) über die man später wieder auf die Objekte zugreifen kann.

So bedeutet ``r.fill_color = (255, 0, 0)`` dass wir die Füllfarbe des zuvor mit r benannten Rechtecks ändern.
  
## Umrandung

Jede geometrische Form kann einen **Rand** haben. 
Den Rand kannst du als Integer-Wert mit dem Attribut ``border`` festlegen und die Farbe mit dem Attribut ``border-radius``:

Das folgende Bild erzeugt ein rotes Rechteck mit gelben Rand:

```python
from miniworldmaker import *

board = PixelBoard(350, 150)
r = Rectangle((10,10), 100, 100)
r.fill_color = (255, 0, 0)
r.border = 3
r.border_color = (255, 255,0)

board.run()
```

Ausgabe:

<img src="../_images/processing/border.png" alt="borders" width="260px"/>


## Füllung

Du kannst auch Figuren zeigen, die nur einen Rand aber über keine Füllung besitzen. Das Attribut ``fill`` legt fest, ob ein Objekt eine Füllung hat.

Das folgende Rechteck hat z.B. keine Füllung:

```python
from miniworldmaker import *

board = PixelBoard(350, 150)
r = Rectangle((10,10), 100, 100)
r.fill = False
r.border = 3
r.border_color = (255, 255,0)

board.run()
```

## Das Board


Alle Figuren werden auf einem ``Board`` gezeichnet. Auch das Board hat verschiedene Eigenschaften, die verändert werden können, z.B. Größe und Hintergrundfarbe.

Bachte folgenden Code, welcher Größe und Hintergrund des Boards festlegt.

```python
  from miniworldmaker import *

  board = PixelBoard()
  board.add_background((255,255,255))
  board.size = (400,200)
  r = Rectangle((10,10), 100, 100)
  r.fill = False
  r.border = 3
  r.border_color = (255, 255,0)

  board.run()
```

Ausgabe:

<img src="../_images/processing/board.png" alt="A board" width="260px"/>
