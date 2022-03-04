Appearance: Costume
####################

The 'Costume' class is a child classes of the 'Appearance' class. 

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

    Usually costumes are created with `token.add_costume([image_path|color])`



Costume
=======


.. autoclass:: miniworldmaker.appearances.costume.Costume
   :members:
