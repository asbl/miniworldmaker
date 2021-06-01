Collisions
==========

There are 3 different kind of collisions:

### TileBased Collissions

  * on_sensing_|class|(self, other)
  

### PixelBased Collisisions

  * **on_sensing_|class|(self, other, distance, collision_type)**
  
    If you use a PixelBoard, the sensing_token function checks if two tokens overlap.
 
    The parameter collision_type specifies how collisions should be checked: 

    ```eval_rst
    .. autoattribute:: miniworldmaker.tokens.token.Token.collision_type
       :annotation:
       :noindex:
    ```


### PhysicsBaded Collisions 

  * on_toching_|class|(self, other)
  
  * on_separation_|class|(self, other)