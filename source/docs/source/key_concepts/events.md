Events
======

 ### Keyboard events
 
  * `on_key_down(self, keys)`
  
    Is called when a key is pressed. `keys` is a list of keys.
   
  * `on_key_down_a(self)`
  
    Called when the a key is pressed. You can handle special keys by modifying the key, e.g. `on_key_down_w(self)` or `on_key_down_x(self)`.

  * `on_key_presssed(self, keys)` 
  
    Is called when a key is pressed. `keys` is a list of keys.
    Unlike `on_key_down`, the event is called again and again as long as the key is pressed.
    
    Like `on_key_down` the method can be called in the variant `on_key_pressed_|letter|(self)` (e.g. `on_key_pressed_w(self)`). 
    
  * `on_key_up`(self, keys):
    
    Is called when a key is released. Keys is a list of keys.  
    Like `on_key_up` the method can be called in the variant `on_key_up_|letter|` (e.g. `on_key_up_t(self)`).
   
### Mouse events   
   
  * `on_mouse_left(self)`
  
    Left mouse button was pressed
   
  * `on_mouse_right(self)` 
    
      Left mouse button was pressed
      
  * `on_mouse_motion(self)` 
    
    The mouse is moved
    
  * `on_left_clicked(self)` (can only added to tokens)
  
    A token was clicked on.
    
  * `on_mouse_enter(self)` (can only added to tokens)
  
    The mouse 'enters' a token
      
  * `on_mouse_leave(self)` (can only added to tokens)
  
    The mouse 'leaves' a token      

   
### Collisions

   * `on_sensing_[class name]`(self, other) - 
   
     Checks whether there is a collision with an object of a certain class.
     This only works if the objects overlap.

     The `other` parameter contains the other object with which a collision was detected. 

     E.g.: `ony_sensing_token(self, other)` - This detects collissions with all tokens.
   
   * `on_sensing_borders(self, borders)`: 
   
     The method is called if a collision with a border is detected.
   
      The `borders` parameter contains a list of strings (e.g. `["left", "right"]`) of the detected borders
   
### With physics engine:

-> See more under Physics

  * **on_touching_|class name|** 
   
     Is called when the object touches another one. 
     Unlike **on_sensing_|class name|**, there does not have to be an overlap.
  
  * **on_separation_with_|classname|** 
     
     Is called when two objects separate.
  
### Messages

Messages are used to allow objects to communicate with each other.

  * Send a message:
  
    A token and the board can send a message **to all tokens and the board** with the command: `self.send_message("message_string")` 
 
  * Process a message:
  
    If your board or your token should react to messages you can use the event `on_message`:
    
    ```python
    @player.register
    def on_message(self, message):
        if message = "Example message":
          do_something()
     ```