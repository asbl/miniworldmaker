Boards: Physicsboard
*********************

**PhysicsBoard** is a child class of **Board**


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


.. autoclass:: miniworldmaker.boards.physics_board.PhysicsBoard
   :members:

   .. autoclasstoc::


