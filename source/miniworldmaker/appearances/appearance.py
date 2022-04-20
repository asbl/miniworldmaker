from typing import Union, Tuple

import miniworldmaker.appearances.appearance_base as appearance_base
import numpy
import pygame
import miniworldmaker.tools.color as color


class Appearance(appearance_base.AppearanceBase):
    """Base class of token costumes and board backgrounds

    The class contains all methods and attributes to display and animate images of the objects, render text on the images or display overlays.

    """

    @property
    def font_size(self):
        return self.font_manager.font_size

    @font_size.setter
    def font_size(self, value):
        self.font_manager.font_size = value
        self.reload_transformations_after("write_text")

    def set_font(self, font, font_size):
        self.font_manager.font_path = font
        self.font_manager.font_size = font_size

    def set_animation_speed(self, value):
        self.animation_speed = value

    @property
    def is_textured(self):
        """
        bool: If True, the image is tiled over the background.

        Examples:

            Texture the board with the given image:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                background = board.add_background("images/stone.png")
                background.is_textured = True
                board.run()

            .. image:: ../_images/is_textured.png
                :alt: Textured image>

            Set texture soize

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                background = board.add_background("images/stone.png")
                background.is_textured = True
                background.texture_size = (15,15)
                board.run()

            .. image:: ../_images/is_textured1.png
                :alt: Textured image


        """
        return self._is_textured

    @is_textured.setter
    def is_textured(self, value):
        self._is_textured = value
        self.reload_transformations_after("texture")

    @property
    def is_rotatable(self):
        """If True, costume will be rotated with token direction

        Examples:

            Costume of token t ignoriert aspect-ratio:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                t = Token((600,50))
                t.add_costume("images/alien1.png")
                t.costume.is_scaled = True
                t.size = (140,80)
                t.border = 1

                board.run()

            Output:
            
            .. raw:: html 

                <video loop autoplay muted width=400>
                <source src="../_static/rotatable.webm" type="video/webm">
                Your browser does not support the video tag.
                </video> 

        """
        return self._is_rotatable

    @is_rotatable.setter
    def is_rotatable(self, value):
        self._is_rotatable = value
        self.dirty = 1

    @property
    def is_centered(self):
        """ """
        return self._is_centered

    @is_centered.setter
    def is_centered(self, value):
        self._is_centered = value
        self.dirty = 1

    @property
    def orientation(self):
        """bool: If True, the image will be rotated by parent orientation before it is rotated.

        Examples:

            Both tokens are moving up. The image of t2 is correctly algined. t1 is looking in the wrong direction.

                .. code-block:: python



                    from miniworldmaker import *

                    board = TiledBoard()

                    t1 = Token((4,4))
                    t1.add_costume("images/player.png")
                    t1.move()

                    t2 = Token((4,5))
                    t2.add_costume("images/player.png")
                    t2.orientation = - 90
                    t2.move()

                    @t1.register
                    def act(self):
                        self.move()

                    @t2.register
                    def act(self):
                        self.move()

                    board.run()

            .. image:: ../_images/orientation.png
                :alt: Textured image

        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        self.reload_transformations_after("orientation")

    @property
    def is_flipped(self):
        """Flips the costume or background. The image is mirrored over the y-axis of costume/background.

        Examples:

            Flips actor:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                token = Token()
                token.add_costume("images/alien1.png")
                token.height= 400
                token.width = 100
                token.is_rotatable = False
                @token.register
                def act(self):
                    if self.board.frame % 100 == 0:
                        print("flip")
                        if self.costume.is_flipped:
                            self.costume.is_flipped = False
                        else:
                            self.costume.is_flipped = True
                board.run()

            .. image:: ../_images/flip1.png
                :alt: Textured image

            .. image:: ../_images/flip2.png
                :alt: Textured image

        """
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self._is_flipped = value
        self.reload_transformations_after("flip")

    def flip(self, value):
        self.is_flipped = value

    @property
    def is_scaled(self):
        """Scales the actor to parent-size without remaining aspect-ratio.

        Examples:

            Costume of token t ignoriert aspect-ratio:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                t = Token((600,50))
                t.add_costume("images/alien1.png")
                t.costume.is_scaled = True
                t.size = (140,80)
                t.border = 1

                board.run()

            .. image:: ../_images/is_scaled.png
                :alt: Textured image
        """
        return self._is_scaled

    @is_scaled.setter
    def is_scaled(self, value):
        if value:
            self._is_upscaled = False
            self._is_scaled_to_height = False
            self._is_scaled_to_width = False
        self._is_scaled = value
        self.reload_transformations_after("scale")

    @property
    def is_upscaled(self):
        """If True, the image will be upscaled remaining aspect-ratio.

        Examples:

            Costume of token t ignoriert aspect-ratio:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                t = Token((600,50))
                t.add_costume("images/alien1.png")
                t.costume.is_scaled = True
                t.size = (140,80)
                t.border = 1

                board.run()
        """
        return self._is_upscaled

    @is_upscaled.setter
    def is_upscaled(self, value):
        if value:
            self._is_scaled = False
            self._is_scaled_to_height = False
            self._is_scaled_to_width = False
        self._is_upscaled = value
        self.reload_transformations_after("scale")

    @property
    def is_scaled_to_width(self):
        return self._is_scaled_to_width

    @is_scaled_to_width.setter
    def is_scaled_to_width(self, value):
        if value:
            self._is_upscaled = False
            self.is_scaled = False
            self._is_scaled_to_height = False
        self.is_scaled = False
        self._is_scaled_to_width = value
        self.reload_transformations_after("scale")

    @property
    def is_scaled_to_height(self):
        return self._is_scaled_to_height

    @is_scaled_to_height.setter
    def is_scaled_to_height(self, value):
        if value:
            self._is_upscaled = False
            self.is_scaled = False
            self._is_scaled_to_height = False
        self.is_scaled = False
        self._is_scaled_to_height = value
        self.reload_transformations_after("scale")

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = value
        self.reload_transformations_after("all")
        

    @property
    def coloring(self):
        """
        Defines a colored layer. Coloring is True or false. The color is defined by the attribute appearance.color

        """
        return self._coloring

    @coloring.setter
    def coloring(self, value):
        self._coloring = value
        self.reload_transformations_after("coloring")

    @property
    def transparency(self):
        """Defines a transparency.

        If ``transparency``is ``True``, the che transparency value
        is defined by the attribute ``appearance.alpha``

        """
        return self._transparency

    @transparency.setter
    def transparency(self, value):
        self._transparency = value
        self.reload_transformations_after("transparency")

    @property
    def alpha(self):
        """defines transparency of Token: 0: transparent, 255: visible
        If value < 1, it will be multiplied with 255.

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board(800,400)

                t = Token((600,250))
                t.add_costume("images/alien1.png")
                t.costume.alpha = 50
                t.width = 40
                t.border = 1

                board.run()

            .. image:: ../_images/alpha.png
                :alt: Textured image

        """
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        if value > 0 and value < 1:
            value = value * 255
        if value == 255:
            self.transparency = False
        else:
            self.transparency = True



    def get_text_width(self):
        return self.font_manager.get_font_width()

    def remove_last_image(self):
        self.image_manager.remove_last_image()

    def add_image(self, source: Union[str, pygame.Surface, Tuple] = None) -> int:
        """Adds an image to the appearance


        Returns:
            Index of the created image.

        Examples:

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                token = Token()
                costume = token.add_costume("images/1.png")
                costume.add_image("images/2.png")

                board.run()

        """
        super().add_image(source)

    def add_images(self, sources: list):
        """Adds multiple images to background/costume. 
        
        Each source in sources paramater must be a valid parameter for :py:attr:`Appearance.add_image`
        """
        for source in sources:
            self.add_image(source)

    @property
    def is_animated(self):
        """If True, the costume will be animated.


        .. code-block:: python

            from miniworldmaker import *

            board = Board(80,40)

            robo = Token()
            robo.costume.add_images(["images/1.png"])
            robo.costume.add_images(["images/2.png","images/3.png","images/4.png"])
            robo.costume.animation_speed = 20
            robo.costume.is_animated = True
            board.run()

        .. video:: ../_static/animate.webm
            :autoplay:
            :width: 300
            :height: 100
        """
        return self._is_animated

    @is_animated.setter
    def is_animated(self, value):
        self._is_animated = value

    def count_pixels_by_color(self, rect, color, threshold=(0, 0, 0, 0)):
        """Counts the number of pixels of a color under the appearance.

        Args:
            color: The color
            threshold: The allowed deviation from the color splitted into r,g,b and alpha values.

        Returns: The number of matching pixes

        """
        surf = pygame.Surface((rect.width, rect.height))
        surf.blit(self._image, (0, 0), rect)
        return pygame.transform.threshold(
            dest_surf=None, set_behavior=0, surf=surf, search_color=color, threshold=threshold
        )

    def animate(self):
        """Animates the costume


        .. code-block:: python

            from miniworldmaker import *

            board = Board(80,40)

            robo = Token()
            robo.costume.add_images(["images/1.png"])
            robo.costume.add_images(["images/2.png","images/3.png","images/4.png"])
            robo.costume.animation_speed = 20
            robo.costume.is_animated = True
            board.run()

        .. video:: ../_static/animate.webm
            :autoplay:
            :width: 300
            :height: 100
        """
        self.is_animated = True

    def after_animation(self):
        """
        the method is overwritten in subclasses costume and appearance

        Examples:

            The token will be removed after the animation - This can be used for explosions.

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                token = Token()
                costume = token.add_costume("images/1.png")
                costume.add_image("images/2.png")
                costume.animate()
                @costume.register
                def after_animation(self):
                    self.parent.remove()

                board.run()
        """
        pass


    def reset(self):
        self.image_manager.reset()

    def set_image(self, source) -> bool:
        """Sets the displayed image of costume/background to selected index

        Args:
            index (int): The image index

        Returns:
            True, if image index exists

        Examples:

            Add two images two background and switch to image 2

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                background = board.add_background("images/1.png")
                background.add_image("images/2.png")
                background.set_image(1)
                board.run()

        """
        return super().set_image(source)

    def to_colors_array(self) -> numpy.ndarray:
        """ Create an array from costume or background. 
        The array can be re-written to appearance with ``.from_array``

        Examples:

            Convert a background image to grayscale

            .. code-block:: python

                from miniworldmaker import *

                board = Board(600,400)
                board.add_background("images/sunflower.jpg")
                arr = board.background.to_colors_array()

                def brightness(r, g, b):
                    return (int(r) + int(g) + int(b)) / 3

                for x in range(len(arr)):
                    for y in range(len(arr[0])):
                        arr[x][y] = brightness(arr[x][y][0], arr[x][y][1], arr[x][y][2])
                        
                board.background.from_array(arr)
                board.run()

            Output:

            .. image:: ../_images/sunflower5grey.png
                :alt: converted image
        """
        return pygame.surfarray.array3d(self.image)

    def from_array(self, arr : numpy.ndarray):
        """Create a background or costume from array. The array must be a ``numpy.ndarray, 
        which can be created with ``.to_colors_array``

        Examples:

            Convert grey default-background to gradient

            .. code-block:: python

                from miniworldmaker import *

                board = Board()
                arr = board.background.to_colors_array()
                print(arr)
                for x in range(len(arr)):
                    for y in range(len(arr[0])):
                        arr[x][y][0] = ((x +1 ) / board.width) * 255
                        arr[x][y][1] = ((y +1 ) /board.width) * 255
                board.background.from_array(arr)
                board.run()

                        
                board.background.from_array(arr)
                board.run()

            Output:

            .. image:: ../_images/gradient3.png
                :alt: converted image
        """
        surf = pygame.surfarray.make_surface(arr)
        self.image_manager.replace_image(surf)

    def from_appearance(self, appearance, index):
        self.image_manager.add_image_from_surface(index)



    """def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background.count_pixels_by_color(rect, color, threshold)
    """

    @property
    def color(self):
        """->See fill color"""
        return self._fill_color

    @color.setter
    def color(self, value):
        value = color.Color.create(value).get()
        self._fill_color = value
        # self.reload_costume()

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        """fill color of token"""
        self.color = value

    def fill(self, value):
        """Set default fill color for borders and lines"""
        self._is_filled = value
        if self.is_filled != None and self.is_filled != False and self.is_filled != True:
            self.fill_color = color.Color(value).get()
        self.reload_transformations_after("all")

    @property
    def is_filled(self):
        """Is token filled with color?"""
        return self._is_filled

    @is_filled.setter
    def is_filled(self, value):
        """Defines if costume is filled with a color.

        if ``_is_filled`` set to a color-value, ``self.fill_color`` is set to the color.
        
        """
        self.fill(value)

    @property
    def stroke_color(self):
        """see border color"""
        return self._border_color

    @stroke_color.setter
    def stroke_color(self, value):
        self.border_color = value

    @property
    def border_color(self):
        """border color of token"""
        return self._border_color

    @border_color.setter
    def border_color(self, value : int):
        if value != None:
            self._border_color = value
            self.reload_transformations_after("all")
        else:
            self.border = None

    @property
    def border(self):
        """The border-size of token.

        The value is 0, if token has no border

        Returns:
            _type_: int
        """
        return self._border

    @border.setter
    def border(self, value):
        self._border = value
        self.reload_transformations_after("all")
