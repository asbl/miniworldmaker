Boards: TiledBoard
******************

**TiledBoard** is a child class of **Board**


.. mermaid::

   classDiagram
      BaseBoard <|-- Board
      Board <|-- PixelBoard
      BaseBoard <|-- TiledBoard
      PixelBoard <|-- PhysicsBoard
      class BaseBoard{
      }
      class Board{
      }
      class PixelBoard{

      }
      class TiledBoard{
      }  
      class PhysicsBoard{
      }  

TiledBoard
==========


.. autoclass:: miniworldmaker.boards.tiled_board.TiledBoard
   :members:

   .. autoclasstoc::


