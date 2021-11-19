import miniworldmaker as mwm

board = mwm.PixelBoard(columns=280, rows=100)
board.add_background("images/water.png")
board.speed = 1
# Should show: A1, B1, C1, C2, C3, A1
robo = mwm.Token(position=(0, 0))
costume_a = robo.add_costume()
robo.costume.add_images(["images/a1.png","images/a2.png","images/a3.png"])
costume_b = robo.add_costume(["images/b1.png","images/b2.png","images/b3.png"])
costume_c = robo.add_costume(["images/c1.png","images/c2.png","images/c3.png"])
@costume_c.register
def after_animation(self):
    self.token.switch_costume(costume_a)
    print("after animation")
robo.size = (99, 99)
costume_a.animation_speed = 80
costume_b.animation_speed = 80
costume_c.animation_speed = 80
mwm.ActionTimer(30,robo.animate_costume,costume_b)
mwm.ActionTimer(90,robo.animate_costume,costume_c)
robo.costume.animate()
board.run()


