# Werte und Variablen

Ein `Wert` ist etwas, dass im Computer gespeichert wird und von einem Computer-Programm manipuliert werden kann. Im Folgenden werden Werte als ``Objekte`` bezeichnet und die Wörter werden synonym verwendet.

```{note}
In anderen Programmiersprachen unterscheidet man primitive Datentypen, die nur verändert werden können und **Objekte**, welche oft auch Attribute und Methoden mitbringen, wie z.B. die Klasse ``board``, welche das Attribut ``size`` besitzt und deren Hintergrund mit der Methode `add_background` verwendet werden kann.

Python hat die einfache Philosphie: Alles ist ein Objekt - Daher wird hier generell der Begriff *Wert* verwendet.
```

Jeder Wert hat einen Datentyp, welchen du abfragen kannst, z.B. liefert folgendes Programm:

``` python
from miniworldmaker import *
import random
board = Board((100,100))

print(type("Hello World"))
print(type(Line((10,10), (100,100))))
print(type(17))

board.run()
```

Die folgende Ausgabe auf der Kommandozeile:

```
<class 'str'>
<class 'tokens.shapes.Line'>
<class 'int'>
```

## Variablen

Damit im Computer erstellte Objekte wiedergefunden werden können, muss man speichern, wo diese zu finden ist. Auf technischer Ebene speichert man dazu den *Speicherplatz* eines Objekts im Rechner. In einer Programmiersprache wie Python verwenden wir einen Namen um Objekte wiederzufinden.

``` python
line = Line((10,10), (100,100))
```

speichert die Linie unter dem Namen line. Wenn du jetzt den Namen line verwendest, kannst du auf die Variable zugreifen und das Objekt verändern.

Du hast z.B. in den vorherigen Kapiteln schon die Farbe einer Linie verändert:

``` python
line.fill_color = (255,0,0)
```

Genauso kannst du z.B. auch mit Zahlen rechnen

``` python
a = 3
b = 4
print(a + b)
```

## Zuweisungen

Zuweisungen schreibt man als:

``` python
c = a + b
```
Die bedeutet:

  - Zuerst wird das Ergebnis auf der rechten Seite ausgewertet.

  - Dann wird das Ergebnis in die Variable auf der linken Seite gespeichert.

Nach folgendem Programm:

``` python
a = 3
b = 4
c = a + b
```

hat a den Wert 3, b den Wert 4 und c den Wert 7.

Genauso kannst du aber auch Werte von Objekten, z.B. die Position eines Kreises verändern. Das folgende Programm lässt dich einen Kreis mit den Tasten a und d nach links oder rechts bewegen. Die x-Position ist über den Namen ``circle.x`` zugreifbar und kann auch so verändert werden.

``` python
from miniworldmaker import *
import random
board = Board((100,100))

circle = Circle((50,50), 20)

@board.register
def on_key_pressed_a(self):
    circle.x = circle.x - 1

@board.register
def on_key_pressed_d(self):
    circle.x = circle.x + 1
    
board.run()
```

Die Zeile ``circle.x = circle.x + 1`` sagt folgendes: Berechne zuerst den Wert ``circle.x + 1`` (d.h. erhöhe die x-Koordinate des Kreises um 1.) und speichere das Ergebnis dieser Berechnung wieder in ``circle.x``.

```{note}
Das = bedeutet nicht das der Ausdruck links und rechts mathematisch gleich ist. 
Stattdessen wird das Ergebnis der rechten Seite zuerst ausgewertet und das Ergebnis dieser Berechnung in die Variable auf der linken Seite gespeichert.

Man liest den Ausdruck ``a = b`` als b wird a **zugewiesen**.

Manche Programmiersprachen verwenden statt dem = Zeichen ein anderes Zeichen um Verwirrung bei Programmieranfängern zu vermeiden.
```

## Verwendung

Überall wo du bisher eine Zahl oder einen Text verwendet hast, kannst du auch direkt Variablen einsetzen, z.B.

``` python
a = 3
b = 4
line = Line((a, b), (5, 6))
``` 

Dies funktioniert immer dann, wenn der **Datentyp** der Variablen mit dem erwarteten **Datentyp** übereinstimmt. 


Folgender Code z.B. führt z.B. zu einem Fehler:

``` python
a = 3
b = 4
line = Line(a, (5, 6))
``` 

Line erwartet ein Tupel und erhält aber nur eine Integer-Variable. Daher wird folgender Fehler ausgegeben

```
miniworldmaker.exceptions.miniworldmaker_exception.TokenArgumentShouldBeTuple: First argument to create a Token [position] should be a Tuple. 
```

Der Fehler versucht dir einen Hinweis zu geben, was du falsch gemacht hast, oft hilft es also die Fehlermeldungen zu lesen.


## Gültigkeitsbereich - Scope

Wenn Programmierer größere Programme schreiben -und das auch oft im Team-, dann kommt dem Namen von Variablen eine besondere Bedeutung zu: Wie verhindert man, dass andere Programmierer die eigenen Variablennamen verwenden und dadurch sogar unvorhergesehene Nebenwirkungen verursachen können?

Die Antwort darauf sind "Gültigkeitsbereiche: Eine Variable hat unterschiedliche Gültigkeitsbereiche, je nachdem wo sie definiert wurde:

  * Eine Variable die innerhalb einer Funktion eingeführt wird hat einen lokalen Gültigkeitsbereich. Sie ist innerhalb dieser Funktion **lokal** sichtbar, aber nicht innerhalb von anderen Funktionen.

  * Eine Variable die außerhalb einer Funktion definiert wurde, ist **global** sichtbar und kann in allen Funktionen deines Programms verwendet werden. **Achtung**: Wenn man auf globale Variablen zugreifen und diese verändern will, muss man das Schlüsselwort global verwenden.

  Folgendes funktioniert:

  ``` python
  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      print(a)
  board.run()
  ```
  
  Es wird der Wert 3 ausgegeben.

  ````{warning}
  Dies funktioniert aber nicht, da bei der Zuweisung a als lokale Variable interpretiert wird (die nicht definiert wurde)

  ``` python

  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      a = a + 1
      print(a)
  board.run()
  ```
  ````
  
  Dies funktioniert wieder, da a als globale Variable definiert wird und daher auch auf die globale Variable zugegriffen wird.

  ``` python

  from miniworldmaker import *
  board = Board((100,100))
  a = 3
  @board.register
  def on_key_pressed_a(self):
      global a
      a = a + 1
      print(a)
  board.run()
  ```


