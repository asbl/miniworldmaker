Physics
=======

### Bestandteile:

  * **PhysicsBoard** - A board class that automatically loads all objects into the physics engine.
  * **token.setup_physics()** - Here you can define the physical properties of a token. The method is called before on_setup().
If you are not using a PhysicsBoard, the first object with this method initializes the physics engine. All objects with 
the method setup_physics() are then simulated with the physics engine.

### Physikalische Eigenschaften

  * **token.physics.mass**(int; 1) The mass of the token. Default: 1
  * **token.physics.gravity**(bool; true): Should the token follow the laws of physics?
  * **token.physics.stable** (bool; true): Can the token rotated by the laws of physics? 
  * **token.physics.friction** (int; 10): When surfaces are in contact to each other, the driction removes the kinetic energy.
  * **token.physics.can_move** (bool; true): When surfaces are in contact to each other, the friction removes the kinetic energy. 
  * **token.physics.elasticity** (int; 0.5): How much should other objects bounce off the token?
  