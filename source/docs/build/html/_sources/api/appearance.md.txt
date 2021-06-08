Appearance
============================

**Appearance** is the base class for **Costume** and **Background**

The Appearance class contains all the logic common to both, e.g. scaling and rotating images. The child classes contain the actions that are specific to these classes (e.g. certain overlays).

All actions performed on the images can be found in the class ImageRenderer

::::{important}
You do not need this class. If you work with tokens, then you use the child class **Costume**. If you work with the board, you use the child class **Background**.
::::

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

### Appearance

```{eval-rst}
.. autoclass:: miniworldmaker.appearances.appearance.Appearance
   :members:
```