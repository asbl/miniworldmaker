Physik
======

MiniWorldmaker hat eine integrierte Physik-Umgebung.

![tiles](/_images/physics2.gif)

## Physikalische Eigenschaften eines Tokens

Du kannst die physikalischen Eigenschaften eines Tokens ändern, z.B.:

```
self.line1 = Line((0, 100), (400, 900), 5, color=(100, 100, 255))
self.line1.physics.elasticity = 0.4
```

Damit das Objekt von der Physik-Engine kontrolliert wird, musst du einmalig aufrufen:

```
self.line1.start_physics()
```

## Objekte bewegen

Wenn du Objekte bewegen willst, kannst du ihnen einen "Impuls geben". Der Impuls wird automatisch in **Blickrichtung** gegeben. Willst du die Richtung steuern, musst du vorher die Ausdrichtung des Tokens ändern.

```
circle = Circle((random.randint(40,100), 20), 20, 0,(100,100,100))
circle.direction = -30
circle.physics.impulse_in_direction(300)
```

Alternativ kannst du die Beschleunigung in y-Richtung und in x-Richtung mit `velocity_x` und `velocity_y` auch selbst setzen

```
circle = Circle((random.randint(40,100), 20), 20, 0,(100,100,100))
circle.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50
```


> Mehr Infos: [Physik](../key_concepts/physics.md)