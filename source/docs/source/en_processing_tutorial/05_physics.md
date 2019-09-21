physics
------

MiniWorldmaker has an integrated physics environment.

To physically simulate an object, you must overwrite the method **setup_physics()**.

Example:
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

If the method is implemented, the physics engine is initialized before executing the setup() method.
Once the engine is initialized, you can "push" objects. This works like this:
```
class Ball(Circle):

    def on_setup(self):
        self.direction = 30
        self.physics.impulse_in_direction(300)
```

or like this:
```
class Bird(Actor):

    def on_setup(self):
        ...
        self.physics.velocity_x = 600
        self.physics.velocity_y = - self.board.arrow.direction * 50
```
