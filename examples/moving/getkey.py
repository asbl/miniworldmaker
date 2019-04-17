import pygame
import miniworldmaker


class MyGrid(miniworldmaker.PixelBoard):
    def __init__(self):
        super().__init__(columns=29, rows=1)

    def get_event(self, event: str = None, data=None):
        keys_pressed = pygame.key.get_pressed()
        for index, item in enumerate(keys_pressed):
            if item:
                print(index)



mygrid = MyGrid()
mygrid.show()
