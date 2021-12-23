import miniworldmaker

myboard = miniworldmaker.PhysicsBoard((800,600))
myboard.add_background("images/bg.jpg")
podest = miniworldmaker.Rectangle((380,420), 20, 100, 0)
podest.physics.simulation = "static"
seesaw = miniworldmaker.Rectangle((100,400), 600, 10, 0)
seesaw.physics.density = 50
tree = miniworldmaker.Token((100, 300))
tree.add_costume("images/tree.jpg")
tree.size = (160,160)
tree.physics.size = 0.85, 0.85
tree.physics.density = 1

rock = miniworldmaker.Circle((600, 20), 8, 0)

@miniworldmaker.timer(frames = 100)
def another_rock():
    rock = miniworldmaker.Circle((600, -50), 100, 0)
    rock.physics.density = 800

myboard.run()