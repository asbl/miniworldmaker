Movements
==========

### Directions

An actor can move in different directions. First you need to know how angles are interpreted in Miniworldmaker.
Angles are independent of the orientation of the character:

![movement](/_images/movement.jpg)

  * 0° means a movement to the right.
  
  * 90° means a movement upwards (etc.).
  
### Angles as Strings

Some angle sizes can also be called strings:

  * right": is equivalent to 0°.
  
  * "up" is equivalent to 90°.
  
  * "left" is equivalent to 180°.
  
  * Down is equivalent to 270 degrees.

A special specification is "forward": In contrast to the other specifications, "forward" means
 in the direction of the figure's gaze. In the picture above "forward" corresponds to 0°, because the actor looks to the right.

### Functions to change direction

You can use the following functions to change the alignment of an actor:

  * self.direction = ... Sets the direction directly according to the above rules.
  
  * self.turn_left(degrees): The actor turns degrees to the left.
  
  * self.turn_right(degrees): The actor rotates degrees degrees to the right.
  
  * self.flip(): The actor rotates 180°. The figure is mirrored so that the actor is not upside down after the rotation.
  
  
### Movement

The central function for moving is the move function.

Move has the following signature:

```
    def move(distance) -> BoardPosition:
```

This means
  
  * By default, an actor moves **self.speed** steps in the direction he's looking.
  
  * You can also set the distance it moves manually by using an integer value for the parameter distance.
  
  * The function returns the position on the playing field where the player is after the move.