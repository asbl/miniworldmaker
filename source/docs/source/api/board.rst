Board
*****

.. mermaid::

   classDiagram
      Board <|-- PixelBoard
      Board <|-- TiledBoard
      class Board{
      }
      class PixelBoard{

      }
      class TiledBoard{
      }  


.. warning::
   You do not need instances of this class. Use the subclasses `TiledBoard` and `PixelBoard`


Board
=====

.. autoclass:: miniworldmaker.boards.board.Board
   :members:
   :exclude-members: add_to_board, handle_event


