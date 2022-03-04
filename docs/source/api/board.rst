Boards: BaseBoard
********************

BaseBoard is the base class for boards. If you use boards in your project, you should create instances of `Board` or `TiledBoard`

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


.. warning::
   If you instanciate a `Board`, it will be handled as `PixelBoard``. You can't create instances of BaseBoard


Board
=====

.. autoclass:: miniworldmaker.boards.base_board.BaseBoard
   :members:
   :exclude-members: add_to_board, handle_event


