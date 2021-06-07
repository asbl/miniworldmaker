Physik
======

MiniWorldmaker hat eine integrierte Physik-Umgebung.

![tiles](_images/physics2.gif)

## Physikalische Eigenschaften eines Tokens

Du kannst die physikalischen Eigenschaften eines Tokens direkt ändern, z.B.:

```
self.line1 = Line((0, 100), (400, 900), 5, color=(100, 100, 255))
self.line1.physics.elasticity = 0.4
```

## Objekte bewegen

Wenn du Objekte bewegen willst, kannst du ihnen einen "Impuls geben".

```
circle = Circle((random.randint(40,100), 20), 20, 0,(100,100,100))
circle.physics.impulse_in_direction(300)
```

```
circle = Circle((random.randint(40,100), 20), 20, 0,(100,100,100))
circle.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50
```

## Alternative: Token-Klassen mit Physik

Alternativ kannst du 


Mehr Infos: [Physik](../key_concepts/physics.md)