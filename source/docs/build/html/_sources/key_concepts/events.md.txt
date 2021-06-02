Events
======

 ### Keyboard events
 
  * **on_key_down(self, keys)** 
  
    Is called when a key is pressed. Keys is a list of keys.
   
  * **on_key_down_a(self)**
  
    Called when the a key is pressed. You can handle special keys by modifying the key, e.g. on_key_down_w or on_key_down_x.

  * **on_key_presssed(self, keys)** 
  
    Is called when a key is pressed. **keys** is a list of keys.
    Unlike **on_key_down**, the event is called again and again as long as the key is pressed.
    
    Like **on_key_pressed** the method can be called in the variant **on_key_pressed_|letter|**. 
    
  * **on_key_up**(self, keys):
    
    Is called when a key is released. Keys is a list of keys.  
    Like **on_key_up** the method can be called in the variant **on_key_up_|letter|**.
   
### Mouse events   
   
  * **on_mouse_left(self)** 
  
    Left mouse button was pressed
   
  * **on_mouse_right(self)** 
    
      Left mouse button was pressed
      
  * **on_mouse_motion(self)** 
    
    The mouse is moved
    
  * **on_left_clicked(self)** (Tokens only)
  
    A token was clicked on.
    
  * **on_mouse_enter(self)** (Tokens only)
  
    The mouse 'enters' a token
      
  * **on_mouse_leave(self)** (Tokens only)
  
    The mouse 'leaves' a token      

   
### Collisions

   * **on_sensing_[class name]**(self, other) - 
   
     Checks whether there is a collision with an object of a certain class.
   This only works if the objects overlap.
   
     The **other** parameter contains the other object with which a collision was detected. 
   
   * **on_sensing_borders(self, borders)**: 
   
   The method is called if a collision with a border is detected.
   
   
With physics engine:

-> See more under Physics

  * **on_touching_|class name|** 
   
     Is called when the object touches another one. 
     Unlike **on_sensing_|class name|**, there does not have to be an overlap.
  
  * **on_separation_with_|classname|** 
     
     Is called when two objects separate.
  
### Messages

Messages are used to allow objects to communicate with each other.

  * Send a message:
  
    You can send a message with the command: **self.send_message("Message")** 
  Both the board and a token have this method.
  
  * Process a message:
  
    Use the method: 
    
    ```
    @player.register
    def on_message(self, message):
        pass
     ```