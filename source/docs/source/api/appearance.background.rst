Appearance: Background
######################

The 'Background' class is a child classes of the 'Appearance' class. 

.. mermaid::

   classDiagram
      Appearance <|-- Costume
      Appearance <|-- Background
      Token o-- Appearance
      class Token{
          +add_costume()
      }
      class Appearance{
          +add_image(str)
      }
      class Costume{
      }
      class Background{

      }   

.. note::

    Usually backgrounds are created with `board.add_background([image_path|color])`


Background
**********

.. autoclass:: miniworldmaker.appearances.background.Background
   :members:
