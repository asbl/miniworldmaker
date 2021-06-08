Appearance.Costume
============================

The 'Costume' class is a child classes of the 'Appearance' class. 

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
Since costumes are bound to tokens, you **don't** need to instantiate costume objects directly.
Instead use `token.add_costume()`
:::

### Costume

```{eval-rst}
.. autoclass:: miniworldmaker.appearances.costume.Costume
   :members:
```