import random
import miniworldmaker

board= miniworldmaker.PixelBoard(800, 600)
board.add_background((255, 255, 255, 255))
lst = []
for i in range(50):
    lst.append(miniworldmaker.Circle((random.randint(0, 800),
                                      random.randint(200, 600)),
                                      random.randint(40, 80),
                                      0,
                                      color=(100, 0, 255, 100))
                                    )


@board.register
def act(self):
    for circle in lst:
            circle.y -= (81 - circle.radius) / 10

board.run()
