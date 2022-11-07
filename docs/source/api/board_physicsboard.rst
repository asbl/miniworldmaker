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

PhysicsBoard
============


.. autoclass:: miniworldmaker.boards.board_templates.physics_board.physics_board.PhysicsBoard
   :members:

   .. autoclasstoc::


