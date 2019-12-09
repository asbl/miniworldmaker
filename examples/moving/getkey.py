import miniworldmaker
import pygame


class MyGrid(miniworldmaker.PixelBoard):

    def get_event(self, event: str = None, data=None):
        keys_pressed = pygame.key.get_pressed()
        for index, item in enumerate(keys_pressed):
            if item:
                print(index)



mygrid = MyGrid(29, 1)
mygrid.show()
