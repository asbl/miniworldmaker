from gamegridp import actor
from gamegridp import gamegrid
import pygame


class MyGrid(gamegrid.GameGrid):
    def listen(self, event: str = None, data=None):
        keys_pressed = pygame.key.get_pressed()
        for index, item in enumerate(keys_pressed):
            if item:
                print(index)



mygrid = MyGrid("My Grid", cell_size=40, columns=29, rows=1,
                margin=0)
mygrid.show()
