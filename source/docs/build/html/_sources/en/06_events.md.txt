events
===========

There are several important methods that you can fill with content:

Special Event Methods
-------------------------

### The act() method

The Act method is called again and again at short intervals. 
Here you can place code that should be executed over and over again, e.g:
```
    def act(self):
        if not self.look_on_board(direction = "forward"):
            self.turn_left(90)
        self.move()
```

The Actor looks one square forward and checks whether it is still on the playing field. 
If so, he moves one square forward. Otherwise he turns 90° to the left.

### Sensing methods

Each time an actor detects something different, its corresponding sensing methods are called:

  **on_sensing_tokens(token_list)**: Tracks all tokens at the same location.
  **on_sensing_borders(borders)**: Returns a list of borders that are currently touched (e.g. ["right", "top"]).
  **on_sensing_on_board()**: Called when the player is on the field.
  **on_sensing_not_on_board()**: Called when the player is not on the field.
  
General event handling with the get_event method
----------------------------------------------------

### The get_event(event, data) method

The get_event(event, data) method) is used to react to events of various kinds.

  * The parameter **event** always contains a string with the event, for example:
    * mouse-left": The left mouse button was pressed.
    * ...
    
  * The **data** parameter contains information that matches the event.
    * mouse-left", "mouse-right" : The tile on the board that was clicked.
    
#### Example:

```
    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.move(direction="up")
            elif "S" in data:
                self.move(direction="down")
            elif "A" in data:
                self.move(direction="left")
            elif "D" in data:
                self.move(direction="right")
```

The code checks whether the event "key_down" was thrown.
The parameter data returns a list with all buttons pressed at this moment.
It can therefore be checked: **If* the button X was pressed, do ... 

Translated with www.DeepL.com/Translator