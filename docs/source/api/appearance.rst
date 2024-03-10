Appearance
##########

**Appearance** is the base class for **Costume** and **Background**

The Appearance class contains all the logic common to both, e.g. scaling and rotating images. The child classes contain the actions that are specific to these classes (e.g. certain overlays).

All actions performed on the images can be found in the class ImageRenderer

.. warning::
    
    You do not need instances of this class. 
    
    * If you work with tokens, then you use the child class **Costume**. 
    
    * If you work with the board, you use the child class **Background**.


Appearance
==========

.. autoclass:: miniworldmaker.appearances.appearance.Appearance
   :members:

   .. autoclasstoc::
