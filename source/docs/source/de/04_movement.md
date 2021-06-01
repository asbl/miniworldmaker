Bewegung
==========

### Die Move-Funktion

Die zentrale Funktion zum Bewegen ist die Funktion move

Move hat folgende Signatur:

```
    def move(distance) -> BoardPosition:
```

Dies bedeutet:
  
  * Standardmäßig bewegt sich ein Akteur um **player.speed** Schritte in die Richtung in die er gerade schaut.
  
  * Du kannst die Distanz die er sich bewegt aber auch manuell festlegen, indem du für den Paramter distance einen Integer-Wert einsetzt.
  
  * Die Funktion gibt als Rückgabewert die Position auf dem Spielfeld zurück, an der sich der Akteur nach dem Zug befindet.
  
--> Mehr Infos über Bewegungen: [Movement](../key_concepts/movement.md)
  
### Die Richtung ändern

Die Richtung ändern kannst du mit folgenden Befehlen:

  * **player.turn_left(degrees) - Dreht das Token um *degrees* Grad nach links.
  
  * **player.turn_right(degrees) - Dreht das Token um *degrees* Grad nach rechts.
  
  * **player.point_in_direction(direction) - Dreht das Token in die Richtung *direction*.
  
--> Mehr Infos über Richtungen: [Directions](../key_concepts/directions.md)