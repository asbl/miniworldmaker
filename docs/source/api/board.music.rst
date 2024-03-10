Board.music
***************

`` Board.music`` handles Music in your miniworlder.

You can add a music with:

.. code-block:: python

    if board.music.is_playing():
        board.music.play(path)

When you call music.play() with the path to a new piece of music,
the current music is paused and the new music is started.

.. autoclass:: miniworldmaker.boards.board_manager.board_music_manager.BoardMusicManager
   :members:

   .. autoclasstoc::


