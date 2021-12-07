Board: PixelBoard
##################

**PixelBoard** is a child class of **Board**


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

PixelBoard
==========


.. autoclass:: miniworldmaker.boards.pixel_board.PixelBoard
   :members:


