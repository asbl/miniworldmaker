import miniworldmaker

board = miniworldmaker.PixelBoard()
board.add_background("images/soccer_green.jpg")
board.size = (800,300)
board.background.is_scaled_to_width = True
# 4 tokens: In topleft corner, at (20,20)
t1 = miniworldmaker.Token(position=(0, 0))
t2 = miniworldmaker.Token(position=(60, 40))
t2.add_costume("images/char_blue.png")
t3 = miniworldmaker.Token(position=(100, 40))
t3.add_costume("images/char_blue.png")

t4 = miniworldmaker.Token()
t4.center=(20, 20)
t4.add_costume((100,100,100,200))
print(t4.position)
print(t4.center)

board.run()
