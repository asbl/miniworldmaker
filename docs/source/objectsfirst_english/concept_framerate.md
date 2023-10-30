## Concept: Frame rate


You can set how often `act()` is called by configuring the `board.fps` and `board.speed` attributes.

* `board.fps` defines the `frame rate`. Analogous to a flipbook, where you turn the pages at a fixed speed,
  the frame rate defines how many times per second the image is redrawn.
  `board.fps` has the default value 60, i.e. 60 frames per second are displayed.
  
* In the attribute `board.frame` the current frame is stored. The frames since program start are counted up.
  
* `board.speed` defines how often the program logic (e.g. act) is called per second.
  A value of 60 means that the act() method is called every 60th frame.


``` python
  import miniworldmaker as mwm

  board = mwm.Board()
  board.size = (120,210)

  @board.register
  def on_setup(self):
      board.fps = 1
      board.speed = 3
      
  @board.register
  def act(self):
      print(board.frame)

  board.run()
```

The program above has the output:

```
  3
  6
  9
  12
  15
```

It is counted up very slowly, because exactly one frame per second is played and every 3. frame
(so every 3 seconds) the function `act()` is called.