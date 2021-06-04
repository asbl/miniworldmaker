Collisions
==========

There are 3 different kind of collisions:

  * **Tile-Collisions**: Objects collide when they are in the same tile
  * **Pixel-Collisions**: Collisions are compared with rectangles or by pixel
  * **Physic-Collisions**: Collisions are handled by the physics-engine.

### TileBased Collisions

Method: **on_sensing_token(self, other_token)**

The method is called when the object is sensing another token.
The argument **other_token** can be used to do something with the other token.

  
#### Example

Object bases approach:

```
@laser.register
def on_sensing_token(self, other_token):
    token.remove()
    explosion = miniworldmaker.Token()
    explosion.position = (self.x, self.y)
    ...
```

### PixelBased Collisions

...


### PhysicsBaded Collisions 
...