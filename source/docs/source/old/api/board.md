Board
======

Board is the base class of TiledBoard and PixelBoard. It

```{eval-rst}
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
```

::::{important}
You do not need this class. Use the subclasses `TiledBoard` and `PixelBoard`
::::

## Board

```{eval-rst}
.. autoclass:: miniworldmaker.boards.board.Board
   :members:
   :exclude-members: add_to_board, handle_event
```


