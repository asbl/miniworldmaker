Boards: Board
*************

```Board`` is the base class for boards.

.. mermaid::

   classDiagram
      BaseBoard <|-- Board
      Board <|-- PixelBoard
      Board <|-- TiledBoard
      PixelBoard <|-- PhysicsBoard
      class BaseBoard{
      }
      class Board{
      }
      class TiledBoard{
      }  
      class PhysicsBoard{
      }  


.. warning::

   If you instanciate a `Board`, it will be handled as `PixelBoard``. You can't create instances of BaseBoard


Board
=====

.. autoclass:: miniworldmaker.boards.board.Board
   :members:
   :exclude-members: add_to_board, handle_event

   .. autoclasstoc::



