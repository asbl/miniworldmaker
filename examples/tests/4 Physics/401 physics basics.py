import random
import miniworldmaker as mwm

board = mwm.PhysicsBoard((800, 600))
#board.gravity = (0, 900)
print("board", board.gravity, board.space.gravity)
board.add_background("images/background.png")

a = mwm.Token()
a.size = (40,40)
a.position = (75, 200)
a.add_costume("images/fly.png")

print("my costume", a.costume.image)
a.physics.simulation = "simulated"
a.size = (40, 40)
print(a.width, a.height)
print("-----> set shape to circle")
a.physics.shape_type = "circle"
print("token gravity", a.physics._gravity)


b = mwm.Token()
b.position = (75, 400)
b.add_costume("images/fly.png")
b.physics.simulation = "manual"


c = mwm.Token()
c.position = (275, 200)
# c.size = (40,40)
c.add_costume("images/fly.png")
c.physics.simulation = "simulated"



d = mwm.Token()
d.position = (275, 400)
d.add_costume("images/fly.png")
d.physics.simulation = "static"
print("body", d.physics._body, d.physics._gravity, d.physics._can_move, d.physics._stable)


board.start()


board.run()


