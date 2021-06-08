Appearance.Background
============================

The 'Background' class is a child classes of the 'Appearance' class. 

```{eval-rst}
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
```

:::{important}
Since backgrounds are bound to board, you **don't** need to instantiate backgrounds objects directly. Instead use `token.add_costume()`
:::

### Background

```{eval-rst}
.. autoclass:: miniworldmaker.appearances.background.Background
   :members:
```