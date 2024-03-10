# Bildbearbeitung

## Was sind Bilder

Bilder bestehen aus winzig kleinen Pixeln, die alle eine bestimmte Farbe haben:

![sunflower](../_images/sunflower.png)

Bildbearbeitung besteht darin, diese Pixel nach bestimmten Kriterien zu verändern und zu manipulieren.

Dazu benötigen wir `Arrays` die eine spezielle Form von Listen sind (Arrays haben begrenze Größen).

## Laden des Hintergrunds

Im miniworldmaker können wir den `Hintergrund`  mit der Funktion 
`arr = background.to_colors_array()`
laden.

Wenn wir z.B. dieses minimale Programm schreiben:

```python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
print(arr)
board.run()
```

, dann bearbeiten wir im folgenden den Standard-Hintergrund:

![grey](../_images/grey_bg.png)

Du erhälst ein verschachteltes, zweidimensionales Array, das folgendermaßen aussieht:

```
[[[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]

 [[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]

 [[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]

 ...

 [[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]

 [[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]

 [[150 150 150]
  [150 150 150]
  [150 150 150]
  ...
  [150 150 150]
  [150 150 150]
  [150 150 150]]]
```

Die innerste Liste steht jeweils für ein 3-Tupel an Farben. [150, 150, 150]. 

Diese beschreiben jeweils den rot, grün und blau-Anteil des jeweiligen Pixels. Jede Farbe wird durch "Mischen" dieser 3 Grundfarben erzeugt:

![rgb](../_images/processing/rgb.png)

Der Minimalwert für jede Farbe ist 0, der Maximalwert ist 255.

Das Bild-Array besteht:

* Aus einer Liste von Spalten
* und jede dieser Spalten enthält für jede Zeile einen Farbwert (der selbst wiederrum eine Liste mit 3 Werten ist)

![array](../_images/array1.png)

## Verändern des Hintergrunds

Man kann über dieses Array folgendermaßen iterieren:

``` python
from miniworldmaker import *
grey
board = Board()
arr = board.background.to_colors_array()
for x in range(len(arr)): # iterate over all rows
    for y in range(len(arr[0])): # iterate over all columns of row
        arr[x][y][0] = 0
print(arr)
board.run()
```

Die Zählervariable x iteriert über die Spalten und wählt jeweils eine Spalte aus. 
Über jede ausgewählte Spalte wird nun mit der Zählervariablen y iteriert:

![array](../_images/array2.png)

Mit der Anweisung `arr[i][j][0] = 0` wird jeweils die erste Farbe, also der rot-Anteil auf 0 gesetzt.
Das Array sieht folgendermaßen aus:

```
[[[  0 150 150]
  [  0 150 150]
  [  0 150 150]
  ...
  [  0 150 150]
  [  0 150 150]
  [  0 150 150]]

 [[  0 150 150]
  [  0 150 150]
  [  0 150 150]
  ...
  [  0 150 150]
  [  0 150 150]
  [  0 150 150]]

 ...

 [[  0 150 150]
  [  0 150 150]
  [  0 150 150]
  ...
  [  0 150 150]
  [  0 150 150]
  [  0 150 150]]]
```

Dieses Array können wir nun wieder mit dem Befehl `background.from_array(arr)` als Hintergrund laden, so sieht das vollständige Programm aus:

``` python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = 0
board.background.from_array(arr)
board.run()
```

...und so sieht das Ergebnis aus. Die Farbe Grau verliert ihre rot-Anteile und wird dadurch grün-bläulich:

![green-blue](../_images/bg_greenblue.png)

Hier haben wir einfach jedem Bildpunkt den rot-Wert 0 zugewiesen. Wir können aber auch jedem Bildpunkt einen Wert zwischen 0 und 255 zuweisen.

Man kann auch anders über diese Liste iterieren und z.B. nur jede zweite Zeile färben:

``` python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
for x in range(0, len(arr),2 ):
    for y in range(len(arr[0])):
        arr[x][y][0] = 0
print(arr)
board.background.from_array(arr)
board.run()
```

![array](../_images/stripes1.png)

Genauso ist es möglich, den Wert Abhängig von der Zählervariablen i zu verwenden - Auf diese Weise kann man Farbübergänge erzeugen, z.B. so
:

``` python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
print(arr)
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = ((x +1 ) / board.width) * 255
board.background.from_array(arr)
board.run()

```

Mit zunehmenden x-Wert steigt der x-Wert an. (x+1) / board.width ergibt einen Wert zwischen 0 und 1. 
Multipliziert man diesen mit 255 erhält man einen Wert zwischen 0 und 255. Ist ein Wert ganz links, ist sein rot-Wert minimal. Ist es ganz rechts, 
ist der rot-Wert maximal.

Man erhält folgenden Farbübergang.

![array](../_images/gradient1.png)

Dies kann man auch mit der y-Variable machen, und das Programm wie folgt erweitern:

``` python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][1] = ((y +1 ) /board.width) * 255
board.background.from_array(arr)
board.run()
```

Oben ist der grün-Wert minimal, unten ist er maximal:

![array](../_images/gradient2.png)

Man kann dies nun zusammensetzen:

```python
from miniworldmaker import *

board = Board()
arr = board.background.to_colors_array()
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = ((x +1 ) / board.width) * 255
        arr[x][y][1] = ((y +1 ) /board.width) * 255
board.background.from_array(arr)
board.run()
```

Man erhält diesen Farbübergang:

![array](../_images/gradient3.png)

## Bildbearbeitung

Bisher haben wir nun einen einfarbigen Hintergrund bearbeitet, aber genau dies geht natürlich auch mit einem Bild als Hintergrund.

Auf diese Weise können wir verschiedene Filter über das Bild legen.

Wir laden z.B. die Sonnenblume von oben als Hintergrundbild:

![array](../_images/sunflower1.png)

```python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = 0
board.background.from_array(arr)
board.run()
```

Da die rot-Werte aus dem Bild entfernt werden, erhält das Bild einen gründlichen Farbton. Wir haben hier also einen ersten Farbfilter geschrieben.
So sieht das Ergebnis aus:

![array](../_images/sunflower2.png)

Als nächstes manipulieren wir die Helligkeit. Dazu können wir sowohl den rot, grün als blau-Wert mit einer Konstante multiplizieren.

```python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()
constant = 2
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = arr[x][y][0] * constant
        arr[x][y][1] = arr[x][y][1] * constant
        arr[x][y][2] = arr[x][y][2] * constant
board.background.from_array(arr)
board.run()
```

Der erste Versuch sieht allerdings so aus!

![array](../_images/sunflower3.png)

Wie ist dies passiert? 

Jeder Farbton hat einen Wert zwischen 0 und 255, beim Multiplizieren wurden allerdings einige unserer Werte größer als 255 und sind daher "übergelaufen".
Du erkennst dies an besonders dunklen Bereichen, die eigentlich hell sein sollten.

Wir müssen also sicherstellen, dass das Ergebnis kleiner als 255 ist, z.B. so:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()
constant = 2
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = min(arr[x][y][0] * constant, 255)
        arr[x][y][1] = min(arr[x][y][1] * constant, 255)
        arr[x][y][2] = min(arr[x][y][2] * constant, 255)
board.background.from_array(arr)
board.run()
```

![array](../_images/sunflower4.png)

# Bildbearbeitung II (mit Funktionen)

## Helligkeit

Oft benötigen wir die Helligkeit eines Pixels. Die "einfachste Methode dies zu berechnen ist den Durchschnitt der r,g und b-Werte zu berechnen:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

print(brightness(arr[10][20]))
 
board.background.from_array(arr)
board.run()
```

In der Funktion brightness müssen die Werte r, g und b zunächst umgewandelt werden:
Es handelt sich um `uint8`-Werte, so dass das Ergebnis niemals größer als 255 werden darf (Ansonsten ensteht ein "Overflow"). Deshalb müssen die Variablen in den Datentyp `int` umgewandelt werden, damit das Ergebnis der Addition auch ein `int`-Wert und damit beliebig groß ist.

Dies können wir nutzen, um jeden Pixel grau zu färben, abhängig von seiner Helligkeit:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

for x in range(len(arr)):
    for y in range(len(arr[0])):
        
        arr[x][y] = brightness(arr[x][y][0], arr[x][y][1], arr[x][y][2])
        
board.background.from_array(arr)
board.run()
```

![sunflower grey](../_images/sunflower5grey.png)

### Farbunterschied und wahrgenommener Farbunterschied

Beim Arbeiten mit Bildern und Tönen ist es wichtig zu wissen, wie wir Menschen diese wahrnehmen.

Die *wahrgenommene* Helligkeit entspricht nicht der hier berechneten Helligkeit. Für die folgenden Zwecke ist die hier verwendete Form zur Berechnung der Helligkeit aber ausreichend.

## Kantenerkennung

Eine wichtige Funktion in der Bildbearbeitung ist das Erkennen von Kanten. Auch in der künstlichen Intelligenz ist dies wichtig,
weil Kantenerkennung ein erster Schritt ist, um Objekte in einem Bild zu erkennen.

### Wie funktioniert Kantenerkennung?

### Helferfunktionen

Um uns auf den eigentlichen Algorithmus zu konzentrieren, verwenden wir einige Helfer-Funktionen:

1. Ist ein Bildpunkt im Bild?:

``` python
def in_array(arr, x, y):
    if x >= 0 and x < len(arr):
        if y >= 0 and y < len(arr[0]):
            return True
    return False
```

2. Gebe alle Nachbarzellen eines Bildpunktes zurück:

``` python
def neighbour_cells(arr, x, y):
    neighbours = []
    for x0 in range(x-1, x+1):
        for y0 in range(y-1, y+1):
            if in_array(arr, x0, y0):
                neighbours.append(arr[x0][y0])
    return neighbours
```

3. Wir bereiten das Bild vor. Mit  `arr.copy()`` können wir eine Kopie des Bildes erstellen, in der wir nur die Helligkeitswerte speichern.

Auf diese Weise müssen wir später nicht mit allen drei Farbwerten rechnen. 


So sieht das Grundgerüst aus:

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()
grey_arr = arr.copy()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

def in_array(arr, x, y):
    if x >= 0 and x < len(arr):
        if y >= 0 and y < len(arr[0]):
            return True
    return False
    

def neighbour_cells(arr, x, y):
    neighbours = []
    for x0 in range(x-1, x+1):
        for y0 in range(y-1, y+1):
            if in_array(arr, x0, y0):
                neighbours.append(arr[x0][y0])
    return neighbours

for x in range(len(arr)):
    for y in range(len(arr[0])):
        grey_arr[x][y] = brightness(arr[x][y][0], arr[x][y][1], arr[x][y][2])
        
board.background.from_array(arr)
board.run()
```

und jetzt ergänzen wir noch den Algorithmus zur Kantenerkennung:

Der Algorithmus funktioniert so: Wir berechnen mit Hilfe der neighbour_cells-Funktion den durchschnittlichen Helligkeitswert aller Nachbarzellen und färben das Bild entsprechend ein.

``` python
from miniworldmaker import *

board = Board(600,400)
board.add_background("images/sunflower.jpg")
arr = board.background.to_colors_array()
grey_arr = arr.copy()

def brightness(r, g, b):
    return (int(r) + int(g) + int(b)) / 3

def in_array(arr, x, y):
    if x >= 0 and x < len(arr):
        if y >= 0 and y < len(arr[0]):
            return True
    return False
    

def neighbour_cells(arr, x, y):
    neighbours = []
    for x0 in range(x-1, x+1):
        for y0 in range(y-1, y+1):
            if in_array(arr, x0, y0):
                neighbours.append(arr[x0][y0])
    return neighbours

for x in range(len(arr)):
    for y in range(len(arr[0])):
        grey_arr[x][y] = brightness(arr[x][y][0], arr[x][y][1], arr[x][y][2])

for x in range(len(arr)):
    for y in range(len(arr[0])):
        neighbours = neighbour_cells(grey_arr, x, y)
        sum_neighbours = 0
        for neighbour in neighbour_cells(grey_arr, x, y):
            sum_neighbours += neighbour[0]
        mean_neighbours = sum_neighbours / len(neighbours)
        diff = grey_arr[x][y][0] - mean_neighbours
        arr[x][y] = (diff, diff, diff)
        
board.background.from_array(arr)
board.run()
```

![sunflower grey](../_images/sunflower6black.png)

Die Farben sind noch invertiert, d.h. wir brauchen eine Funktion, die die Farben erneut invertiert, so dass der schwarze Hintergrund weiß wird und die Kanten statt weiß schwarz werden.

Dies geht so:

``` python
for x in range(len(arr)):
    for y in range(len(arr[0])):
        arr[x][y][0] = 255 - arr[x][y][0]
        arr[x][y][1] = 255 - arr[x][y][1]
        arr[x][y][2] = 255 - arr[x][y][2]
```

![sunflower grey](../_images/sunflower8_edge.png)

Diesen Algorithmus können wir noch auf verschiedene Art verändern verbessern. Eine Möglichkeit ist es, nur Zellen weiß zu färben, die einen gewissen Schwellenwert überschreiten und alle anderen Zellen schwarz, man könnte auch das Feld der Nachbarzellen größer gestalten, ...

Probiere es aus!