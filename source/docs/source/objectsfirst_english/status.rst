Status: Game state/end of game/levels
***********************************

End of game/level change
========================

The following are typical end-of-game/level change actions:

* Clear the playing field
* Stop the game field.

The following commands are available for this:

* `board.stop()`: Stops the game board. No more actions are executed and no more events are queried.
* `board.start()`: This cancels a stop command.
* `board.is_running`: With this variable you can query the state of the board.
* `board.clear()`: This function removes all pieces from the board.
* `board.reset()`: The function clears the current board and creates a new board with all the pieces as they were created in `board.on_setup()`.


Status/Score
==================

* Often you want to show the current score or something similar.

For this the **miniworldmaker** offers you special tokens, e.g. TextTokens or NumberTokens.

  