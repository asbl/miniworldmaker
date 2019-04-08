Bewegungen
==========

### Richtungen

Ein Actor kann sich in verschiedene Richtungen bewegen. Zunächst musst du dazu wissen, wie in Miniworldmaker Winkel interpretiert werden.
Winkel sind unabhängig von der Ausrichtung der Spielfigur:

![movement](/_images/movement.jpg)

  * 0° bedeutet eine Bewegung nach rechts.
  
  * 90° eine Bewegung nach oben (usw).
  
## Winkel als Strings

Einige Winkelgrößen kannst du auch mit Strings bezeichnen:

  * "right": ist äquivalent zu 0°.
  
  * "up" ist äquivalent zu 90°.
  
  * "left" ist äquivalent zu 180°.
  
  * "down" ist äquivalent zu 270°.

Eine spezielle Angabe ist "forward": Im Gegensatz zu den anderen Angaben bedeutet "forward"
 in Blickrichtung der Figur. Im Bild oben entspricht "forward" 0°, da der Akteur nach rechts schaut.

### Funktionen zur Richtungsänderung

Mit folgenden Funktionen kannst du die Ausrichtung eines Akteurs ändern:

  * self.direction = ... : Setzt die Richtung direkt entsprechend der obigen Regeln.
  
  * self.turn_left(degrees): Der Akteur dreht sich um degrees Grad nach links.
  
  * self.turn_right(degrees): Der Akteur dreht sich um degrees Grad nach rechts.  * self.flip(): Der Akteur dreht sich um 180°. Dabei wird die Spielfigur gespiegelt, so dass der Akteur nach der Drehung nicht auf dem Kopf steht.
  
  
### Bewegung

Die zentrale Funktion zum Bewegen ist die Funktion move

Move hat folgende Signatur:

```
    def move(distance) -> BoardPosition:
```

Dies bedeutet:
  
  * Standardmäßig bewegt sich ein Akteur um **self.speed** Schritte in die Richtung in die er gerade schaut.
  
  * Du kannst die Distanz die er sich bewegt aber auch manuell festlegen, indem du für den Paramter distance einen Integer-Wert einsetzt.
  
  * Die Funktion gibt als Rückgabewert die Position auf dem Spielfeld zurück, an der sich der Akteur nach dem Zug befindet.