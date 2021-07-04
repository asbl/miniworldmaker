import miniworldmaker as mwm

board = mwm.PixelBoard(columns=280, rows=100)
board.add_background("images/water.png")
board.speed = 1

robo = mwm.Token(position=(0, 0))
robo.add_costume()
robo.costume.add_images(["images/1.png", "images/2.png","images/3.png","images/4.png"])
mwm.ActionTimer(80,robo.costume.set_image,1)
mwm.ActionTimer(120,robo.costume.set_image,2)
mwm.ActionTimer(150,robo.costume.set_image,3)
robo.costume.animation_speed = 200
board.run()