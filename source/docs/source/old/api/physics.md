Physics
=======


```{eval-rst}
.. mermaid::

   classDiagram
      Token "1" o-- "1" Physics
      class Token{
         physics: Physics
         start_physics()
      }
      class Physics{
         float gravity
         bool stable
         float friction
         bool can_move
         bool elasticity
         float velocity_x
         float velocity_y
         impulse_in_direction(float power)
      }
```


```{eval-rst}
.. autoclass:: miniworldmaker.physics.physics.PhysicsProperty
   :members:
   :exclude-members: simulation_postprocess_token, simulation_preprocess_token
```