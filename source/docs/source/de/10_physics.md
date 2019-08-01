Physik
------

MiniWorldmaker hat eine integrierte Physik-Umgebung.

Damit ein Objekt physikalisch simuliert wird, musst du die Methode **setup_physics()** überschreiben.

Beispiel:
```
class Paddle(Rectangle):
    def setup(self):
        self.size = (10, 80)
        self.costume.is_rotatable = False

    def setup_physics(self):
        self.physics.stable = True
        self.physics.can_move = True
        self.physics.mass = "inf"
        self.physics.friction = 0
        self.physics.gravity = False
        self.physics.elasticity = 1
```

Wenn die Methode implementiert ist, wird die Physik-Engine vor Ausführung der setup()-Methode initialisiert.
Sobald die Engine initialisiert ist kannst du Objekte "anschubsen". Dies geht folgendermaßen:
```
class Ball(Circle):

    def on_setup(self):
        self.direction = 30
        self.physics.impulse_in_direction(300)
```

oder folgendermaßen:
```
class Bird(Actor):

    def on_setup(self):
        ...
        self.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50
```
