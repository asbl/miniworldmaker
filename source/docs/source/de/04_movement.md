Aktionen II - Bewegung und Ausrichtung 
======================================

Mit der `act()`-Methode kannst du Token in regelmäßigen Abständen ansteuern. Jetzt lernst du, wie du deine Token gezielt in eine Richtung bewegen kannst.


## Die move()-Funktion

Die zentrale Funktion zum Bewegen ist die Funktion `move()`

Mit der Funktion `move()` kannst du dein Objekt um einen oder mehrere Schritte bewegen:


### Beispiel

```python
@player.register
def act(self):
    self.direction = 90
    self.move()
```

Das Objekt **player** schaut nun immer wieder nach rechts *(90°, siehe [hier](../key_concepts/directions.md)* und bewegt sich dann einen Schritt nach vorne.


:::{note} 
➥ Mehr Infos über Bewegungen: [Key Concept: Movement](../key_concepts/movement.md)
:::  

### Das Schlüsselwort self

In dem code oben hast du gesehen, dass die Methode act als Parameter das Schlüsselwort `self` erwartet. Alle Methoden die zu einem Objekt gehören erhalten dieses Schlüsselwort immer als ersten Paramerer.

Anschließend kann innerhalb der Methode mit diesem Schlüsselwort auf Attribute und Methoden des Objekts selbst zurückgegriffen werden.

`self.direction = 90` bezieht sich z.B. *auf die eigene* Ausrichtung.

### Die Richtung ändern

Die Richtung kannst du mit folgenden Befehlen ändern:

  * `player.turn_left(degrees)` - Dreht das Token um **degrees** Grad nach links.
  
  * `player.turn_right(degrees)` - Dreht das Token um **degrees** Grad nach rechts.
  
  * `player.direction = degrees`- Gibt dem player-Objekt die absolute Ausrichtung degrees.
  Der Wert degrees kann hier entweder als Zahl oder als Text wie in folgender Grafik angegeben werden (0: oben, 180, unten, 90 rechts, -90 links):

  ![movement](/_images/movement.jpg)

:::{note} 
> ➥ Mehr Infos über Richtungen: [Key Concept:  Directions](../key_concepts/directions.md)
:::

## Ausblick

  * [Vollständiges Beispiel](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tutorial/04%20-%20movement%20and%20direction.py)

  * [Weitere Beispiele](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/2%20Movement)
