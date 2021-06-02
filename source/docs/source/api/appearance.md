Appearance
============================

**Appearance** is the base class for **Costume** and **Background**

The Appearance class contains all the logic common to both, e.g. scaling and rotating images. The child classes contain the actions that are specific to these classes (e.g. certain overlays).

All actions performed on the images can be found in the class ImageRenderer

```{eval_rst}
.. inheritance-diagram:: miniworldmaker.appearances.background.Background miniworldmaker.appearances.costume.Costume
   :top-classes: miniworldmaker.appearances.appearance.Appearance
   :parts: 1
```

### Appearance

```{eval-rst}
.. autoclass:: miniworldmaker.appearances.appearance.Appearance
   :members:
```