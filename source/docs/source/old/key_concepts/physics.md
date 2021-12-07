Physics
=======

## Basics

All objects passed to the physics engine with `object_name.start_physics()` are managed by the physics engine.

You must therefore call this command **before** you give an object a pulse in a direction.

### Physical Properties

Before calling `object_name.start_physics()`. you can change physical properties of the object. You can set the following properties:

  * `object_name.physics.mass`(int; 1) The mass of the token. Default: 1
  * `object_name.physics.gravity`(bool; true): Should the token follow the laws of physics?
  * `object_name.physics.stable` (bool; true): Can the token rotated by the laws of physics? 
  * `object_name.physics.friction` (int; 10): When surfaces are in contact to each other, the driction removes the kinetic energy.
  * `object_name.physics.can_move` (bool; true): When surfaces are in contact to each other, the friction removes the kinetic energy. 
  * `object_name.physics.elasticity` (int; 0.5): How much should other objects bounce off the token?
  
  :::{note}  
>➥ [Example](https://codeberg.org/a_siebel/miniworldmaker/src/branch/main/examples/processing/physics_simulation.py)
:::