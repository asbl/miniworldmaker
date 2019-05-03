Directions
-----------

### Angles

An actor can move in different directions. First you need to know how angles are interpreted in Miniworldmaker.
Angles are independent of the orientation of the character:

![movement](/_images/movement.jpg)

  * 0° means a movement upwards.
  
  * 90° means a movement to the right..
  
  * 180° oder - 180° means a movement downwards.
  
  * -90° means a movement to the right.

The interpretation of directions corresponds to the popular programming language Scratch, see https://en.scratch-wiki.info/wiki/Direction_(value)

There is one exception: The default direction in Miniworldmaker is 0°, i.e. tokens point upwards.
  
### Angles as Strings

Some angle sizes can also be called strings:

  * right": is equivalent to 0°.
  
  * "up" is equivalent to 90°.
  
  * "left" is equivalent to 180°.
  
  * Down is equivalent to 270 degrees.

A special specification is "forward": In contrast to the other specifications, "forward" means
 in the direction of the figure's gaze. In the picture above "forward" corresponds to 0°, because the actor looks to the right.


### Methods and Attributs

You can use the following functions to change the alignment of an actor:

#### self.direction

Sets the direction directly.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: direction
   :noindex:
```

#### self.turn_left

Turns the actor in left direction.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: turn_left
   :noindex:
```

#### self.turn_right

Turns the actor in right direction.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: turn_right
   :noindex:
```

#### self.flip_x

The actor rotates 180°. The figure is mirrored so that the actor is not upside down after the rotation.

```eval_rst
.. autoclass:: miniworldmaker.tokens.actor.Actor
   :members: flip_x
   :noindex:
```