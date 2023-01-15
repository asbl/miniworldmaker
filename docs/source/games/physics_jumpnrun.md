Tutorial: A Jump`n Run with the Physic-Engine
===============================================

In this chapter we will build a Jump`n run with the physics engine. You will learn the following:

* How do I use the physics engine?
* How do I implement a camera that follows the player?
* How do I use sensors to check if a player is on the "ground".
if is located:
* How do I create animations for different situations (walking, jumping, standing, ...)
    
WARNING: Simulation the physics of a plattformer with a physics-engine *may* not be the best solution and can lead 
to many unexpected side-effects. 

### First steps: The Board

Create a Physicsboard:

``` python
from miniworldmaker import *

...

b = PhysicsBoard(400, 400)
#b.debug = True # If you set b.debug to True, you'll see what the physics-engine is "seeing"
b.run()
```

### Create a Token

Now you must create your first token:

``` 
import math 

...

class Player(Rectangle):
    def on_setup(self):
        self.direction = "right"
        self.size = (80,80)
        self.physics.size = (0.8, 0.8)
        self.physics.density = 1
        self.physics.max_velocity_x = 200 # don't run faster than this
        self.physics.friction = 0.7
        self.moment = math.inf # do not rotate
```

With `self.physics`, you can define object attributes like density or friction. With `self.physics.size` you can scale
down the object for the physics-engine. (In the Physicsengine the token will have the size (80 * 0.8, 80 * 0,8) ).

### Add events 

You can add events to the different buttons. Add these methods to your class:

``` python
    def on_key_pressed_d(self):
        self.physics.force_in_direction(90,1000)
    
    def on_key_pressed_a(self):
        self.physics.force_in_direction(-90,1000)
        
    def on_key_down_w(self):
        if self.sensor.detect():
            self.physics.force_in_direction(0,15000)
```

This will applice a force, if you press a or d or an impulse if you jump. You will need to experience the values for the force.
These depend on the mass of your body which is calculated by its size and density.

### Add some objects

Add some objects to play your game (After the definition of your class and before `b.run()`)

``` python
c = Rectangle((0,300),400, 4)
c.physics.simulation = "manual"
c2 = Rectangle((400,360),400, 4)
c2.direction = 10
c2.physics.simulation = "manual"
c2.friction = 1

c3 = Rectangle((400,220),80, 4)
c3.direction = 10
c3.physics.simulation = "manual"

p = Player((20,220))
```

### The sensor

Jumping should only be allowed, if the player is standing on the ground. A sensor can help to detect this.

A sensor is an object attached to a Token, which can detect tokens.

Expand the `on_setup`-Method:

```
    def on_setup(self):
      self.direction = "right"
        self.size = (80,80)
        self.physics.size = (0.8, 0.8)
        self.physics.density = 1
        self.physics.max_velocity_x = 200 # don't run faster than this
        self.physics.friction = 0.7
        self.moment = math.inf # do not rotate
        self.sensor = Sensor(self, (0, 40))
        self.sensor.size = (40, 20)
        self.sensor.visible = False
        self.standing_costume = self.add_costume("images/alien_stand.png")
```

The sensor ist set to `visible` for demonstration and debugging purposes - You can delete this line later.

![Maze Game - First step](/_images/sensor1.png)      

The player should only be able to jump when the sensor touches a token. Extend the event method for this:

``` python 
    def on_key_down_w(self):
        if self.sensor.detect():
            self.physics.force_in_direction(0,10000)
```

### Animations

You need to access the current `state` of the token and detect state-changes. When the state of the token changes
(e.g.: It switches from "standing" to "walking" or "walking" to "jumping" ), the costume will be changed.

First, add some costumes in `on_setup` and add variables to access the current state:

```python
    def on_setup(self):
        self.direction = "right"
        self.size = (80,80)
        self.physics.size = (0.8, 0.8)
        self.physics.density = 1
        self.physics.max_velocity_x = 200 # don't run faster than this
        self.physics.friction = 0.7
        self.moment = math.inf # do not rotate
        self.sensor = Sensor(self, (0, 40))
        self.sensor.size = (40, 20)
        self.sensor.visible = False
        self.standing_costume = self.add_costume("images/alien_stand.png")
        self.walking_costume = self.add_costume(["images/alien_walk1.png","images/alien_walk2.png"])
        self.jumping_costume = self.add_costume("images/alien_jump.png")
        self.old_velocity_x = 0
        self.was_standing = False
        self.was_jumping = False
        self.was_walking = False
```

Now you must add some methods do detect the current state:

``` python
    def is_standing(self):
        return abs(self.physics.velocity_x) < 5 and self.sensor.detect()
    
    def is_walking(self):
        return abs(self.physics.velocity_x) > 5 and self.sensor.detect()
            
    def is_jumping(self):
        return not self.sensor.detect()
    
    def started_jumping(self):
        return (not self.was_jumping) and self.is_jumping()
            
    def started_standing(self):
        return (not self.was_standing) and self.is_standing()
            
    def started_walking(self):
        return (not self.was_walking) and self.is_walking()  
        
  def has_changed_direction(self):
        if self.old_velocity_x >= -5 and self.physics.velocity_x < 0:
            return True
        elif self.old_velocity_x <= 5 and self.physics.velocity_x > 0:
            return True
        else:
            return False
```

Now you can use this to write the `act()`- Method, which will be called, every frame. The act()-Method 
* calls the corresponding methods, if a state has changed.
* Flips the character, if he changes his direction.
* Saves the current state of velcotiy ans state into variables for the next call of act().

```python
    def act(self):
        changed_state = False # ...is false until a state change was detected in current frame.
        # select costume
        if self.started_standing():
            self.start_standing()
            changed_state = True
        elif self.started_walking():
            self.start_walking()
            changed_state = True
        elif self.started_jumping():
            self.start_jumping()
            changed_state = True
        if changed_state or not self.is_standing():
            if self.physics.velocity_x < 1:
                self.is_flipped = True
            else:
                self.is_flipped = False
        # safe current state for next act
        self.old_velocity_x = self.physics.velocity_x
        self.was_jumping = self.is_jumping()
        self.was_standing = self.is_standing()
        self.was_walking = self.is_walking()
```

...and add methods to start jumping/walking/standing, ...:

```
    def start_standing(self):
        self.switch_costume(self.standing_costume)
        self.costume.is_rotatable = False
       
    def start_walking(self):    
        self.switch_costume(self.walking_costume)
        self.costume.is_rotatable = False
        self.costume.animate(loop = True)
            
    def start_jumping(self):
        self.switch_costume(self.jumping_costume)
        self.costume.is_rotatable = False
```

### The camera

If you want the player to move through a scrolling world you need a camera.

Set boundaries for your board:

```python
b = PhysicsBoard(400, 400)
b.boundary_x = 1200
b.boundary_y = 450
```

...and attach the camera to your token:

```python
    def act(self):
        self.board.camera.from_token(self)
        ...
```

Now you're ready:

<video controls loop width=100%>
  <source src="../_static/physicsnrun1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video> 

