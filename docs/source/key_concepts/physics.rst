Physics
#######

Physics Basics
==============

All objects in a `PhysicsBoard` are handled by the physic-engine

Physical Properties
====================

Each physics-object can have the following properties:

* `object_name.physics.mass` (int; 1) The mass of the token. Default: 1
* `object_name.physics.gravity` (bool; true): Should the token follow the laws of physics?
* `object_name.physics.friction` (int; 10): When surfaces are in contact to each other, the driction removes the kinetic energy.
* `object_name.physics.elasticity` (int; 0.5): How much should other objects bounce off the token?

