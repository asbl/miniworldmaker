Physik
------

MiniWorldmaker hat eine integrierte Physik-Umgebung.

![tiles](../_images/physics.jpg)

### Aktivieren der Physik-Engine

Die einfachste Art die Physik-Engine zu aktivieren ist ein **PhysicsBoard** zu verwenden.

Beispiel:
```
my_board = PhysicsBoard(800, 600)
```

...oder als eigene Klasse

```
class MyBoard(PhysicsBoard)

  def on_setup(self)
    ...
    
my_board = MyBoard(800, 600)
my_board.run()
```

### Physikalische Eigenschaften eines Tokens

In der Methode **setup_physics** kannst du die physikalischen Eigenschaften eines Tokens festlegen.

Beispiel:
```
        self.line1 = Line((0, 100), (400, 900), 5, color=(100, 100, 255))
        @self.line1.register
        def setup_physics():
            self.line1.physics.elasticity = 0.4
```

Hinweis: Die Methode wird *vor* **on_setup** ausgeführt.

### Objekte bewegen

Wenn du Objekte bewegen willst, kannst du ihnen einen "Impuls geben".

```
class Ball(Circle):

    def on_setup(self):
        self.direction = 30
        self.physics.impulse_in_direction(300)
```

Alternativ kannst du auch die x- und y-Geschwindigkeit direkt angeben:
```
class Bird(Actor):

    def on_setup(self):
        ...
        self.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50
```

Mehr Infos: [Physik](../key_concepts/physics.md)