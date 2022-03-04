Boards: Board
##################

**Board** is a child class of **BaseBoard**. It is equivalent to **PixelBoard** 


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

PixelBoard
==========


.. autoclass:: miniworldmaker.boards.board.Board
   :members:


