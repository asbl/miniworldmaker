Bewegung
==========

## Die Move-Funktion

Die zentrale Funktion zum Bewegen ist die Funktion **move()**

Mit der Funktion **move()** kannst du dein Objekt um einen oder mehrere Schritte bewegen:


### Beispiel

```
@player.register
def act(self):
    self.point_in_direction(90)
    self.move()
```

Das Objekt **player** schaut nun immer wieder nach rechts *(90°, siehe [hier](../key_concepts/directions.md)* und bewegt sich dann einen Schritt nach vorne.


:::{note} 
➥ Mehr Infos über Bewegungen: [Key Concept: Movement](../key_concepts/movement.md)
:::  
### Die Richtung ändern

Die Richtung ändern kannst du mit folgenden Befehlen:

  * **player.turn_left(degrees)** - Dreht das Token um **degrees** Grad nach links.
  
  * **player.turn_right(degrees)** - Dreht das Token um **degrees** Grad nach rechts.
  
  * **player.point_in_direction(direction)** - Dreht das Token in die Richtung **direction**.

:::{note} 
> ➥ Mehr Infos über Richtungen: [Key Concept:  Directions](../key_concepts/directions.md)
:::

### Beispiele

> [Beispiele](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/tests/moving)