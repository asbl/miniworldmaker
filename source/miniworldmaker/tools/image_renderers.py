import pygame

class ImageRenderer:

    _images_dict = {}  # dict with key: image_path, value: loaded image

    @staticmethod
    def texture(image, parent, appearance):
        background = pygame.Surface(parent.size)
        background.fill((255, 255, 255))
        i, j, width, height = 0, 0, 0, 0
        while width < parent.width:
            while height < parent.height:
                width = i * image.get_width()
                height = j * image.get_height()
                j += 1
                background.blit(image, (width, height))
            j, height = 0, 0
            i += 1
        return background

    @staticmethod
    def upscale(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        if parent.size != 0:
            scale_factor_x = parent.size[0] / image.get_width()
            scale_factor_y = parent.size[1] / image.get_height()
            scale_factor = min(scale_factor_x, scale_factor_y)
            new_width = int(image.get_width() * scale_factor)
            new_height = int(image.get_height() * scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    @staticmethod
    def scale(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        image = pygame.transform.scale(image, parent.size)
        return image

    @staticmethod
    def rotate(image : pygame.Surface, parent, appearance) -> pygame.Surface:

        return pygame.transform.rotate(image, - (parent.direction))

    @staticmethod
    def correct_orientation(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        return pygame.transform.rotate(image, - appearance.orientation )

    @staticmethod
    def flip(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        return pygame.transform.flip(image, appearance.is_flipped, False)

    @staticmethod
    def colorize(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        image = image.copy()
        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(appearance.color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        return image

    @staticmethod
    def crop_image(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        cropped_surface = pygame.Surface(parent.size)
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0), (0, 0, parent.size[0], parent.size[1]))
        return cropped_surface

    @staticmethod
    def write_text(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        if appearance.font_path is None:
            if appearance.font_size == 0:
                font_size = parent.size[1]
            else:
                font_size = appearance.font_size
            my_font = pygame.font.SysFont("monospace", font_size)
        else:
            my_font = pygame.font.Font(appearance.font_path)
        if appearance.color is None:
            color = (0, 0, 0)
        label = my_font.render(appearance.text, 1, appearance.color)
        image.blit(label, appearance.text_position)
        return image

    @staticmethod
    def info_overlay(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        pygame.draw.rect(image, appearance.color,
                         (0, 0, image.get_rect().width, image.get_rect().height), 10)
        # draw direction marker on image
        rect = image.get_rect()
        center = rect.center
        x = rect.right
        y = rect.centery
        pygame.draw.line(image, appearance.color, (center[0], center[1]), (x, y))
        return image

    @staticmethod
    def show_grid(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        i = 0
        while i <= parent.width:
            pygame.draw.rect(image, appearance.color, [i, 0, parent.tile_margin, parent.height])
            i += parent.tile_size + parent.tile_margin
        i = 0
        while i <= parent.height:
            pygame.draw.rect(image, appearance.color, [0, i, parent.width, parent.tile_margin])
            i += parent.tile_size + parent.tile_margin
        return image

    @staticmethod
    def scale_to_tile(image : pygame.Surface, parent, appearance) -> pygame.Surface:
        image = pygame.transform.scale(image, (appearance.tile_size, appearance.tile_size))
        with_margin = pygame.Surface((parent.tile_size + parent.tile_margin, parent.tile_size + parent.tile_margin))
        with_margin.blit(image, (parent.tile_margin, parent.tile_margin))
        return with_margin

    @staticmethod
    def load_image(path, alpha):
        if path in ImageRenderer._images_dict.keys():
            # load image from img_dict
            _image = ImageRenderer._images_dict[path]
        else:
            # create new image and add to img_dict
            if not alpha:
                _image = pygame.image.load(path).convert()
            else:
                _image = pygame.image.load(path).convert_alpha()
            ImageRenderer._images_dict[path] = _image
        return _image