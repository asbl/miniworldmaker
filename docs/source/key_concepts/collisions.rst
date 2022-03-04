Collisions
###########

There are 3 different kind of collisions:

* **Tile-Collisions**: Objects collide when they are in the same tile
* **Pixel-Collisions**: Collisions are compared with rectangles or by pixel
* **Physic-Collisions**: Collisions are handled by the physics-engine.

TileBased Collisions
====================

Method: **on_sensing_token(self, other_token)**

The method is called when the object is sensing another token.
The argument **other_token** can be used to do something with the other token.

  
Example
-------

Object bases approach:

.. code-block:: python

  @laser.register
  def on_sensing_token(self, other_token):
      token.remove()
      explosion = miniworldmaker.Token()
      explosion.position = (self.x, self.y)
      #...


### PixelBased Collisions

...


### PhysicsBaded Collisions 
...

---

### Collisions

* `on_sensing_[class name](self, other)` 
   
  Checks whether there is a collision with an object of a certain class.
  This only works if the objects overlap.

  The `other` parameter contains the other object with which a collision was detected. 

  E.g.: `ony_sensing_token(self, other)` - This detects collissions with all tokens.
   
* `on_sensing_borders(self, borders)`: 
   
  The method is called if a collision with a border is detected.
   
  The `borders` parameter contains a list of strings (e.g. `["left", "right"]`) of the detected borders
   
With physics engine
===================

-> See more under Physics

* **on_touching_|class name|** 
   
  Is called when the object touches another one. 
  Unlike **on_sensing_|class name|**, there does not have to be an overlap.
  
* **on_separation_with_|classname|** 
     
  Is called when two objects separate.