import logging
import sys

import gamegridp


class MyGrid(gamegridp.GameGrid):
    """My Grid with custom setup method."""

    def setup(self):
        robo1 = Robot(grid=self, location=(1, 1), img_action="scale")

        # Draw border
        for i in range(self._grid_rows):
            Wall(grid=self, location=(0, i))
        for i in range(self._grid_rows):
            Wall(grid=self, location=(self._grid_rows - 1, i))
        for i in range(self._grid_columns):
            Wall(grid=self, location=(i, 0))
        for i in range(self._grid_columns - 1):
            Wall(grid=self, location=(i, self._grid_columns - 1))


class Robot(gamegridp.Actor):
    def setup(self):
        self.is_rotatable = True
        self.add_image("images/robo_green.png", "scale", (40, 40))

    def act(self):
        self.move(1)


class Wall(gamegridp.Actor):
    def setup(self):
        self.is_blocking = True
        self.add_image("images/rock.png", img_action="scale")


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mygrid = MyGrid("My Grid", cell_size=60, columns=10, rows=10,
                margin=0, speed=120,
                background_color=(200, 0, 0), cell_color=(0, 0, 255), img_path="images/stone.jpg")
mygrid.show()
