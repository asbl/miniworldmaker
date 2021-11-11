import miniworldmaker

board = miniworldmaker.PixelBoard(200,400)

board.add_background("images/stone.jpg")

# Token 1: Purple in topleft corner
token1 = miniworldmaker.Token(position=(0, 0))
token1.size = (40, 40) # should be in topleft corner

print("-- token 2 --")
# Token 2: purple at position (60, 50) (touching Token 1)
token2 = miniworldmaker.Token(position=(40, 40))
print("before resize", token2.position)
token2.size = (40, 40)
print("after resize", token2.position, token2.size)
print("-- token 3 --")
# Token 3: Below token1, created with Image "1"
token3 = miniworldmaker.Token(position=(40, 80), image="images/1.png")
token3.size = (40, 40)
print(token3.position)

# Token 4: Below token1, created with Image "2" in `on_setup`-Method
class MyToken(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/2.png")

print("--- Token 4--")
token4 = MyToken(position = (40,130))

# Token5: Created with image "3" without file ending
token5 = miniworldmaker.Token(position=(60, 200), image="images/3.png")

# Token6: Created with images "1" and "2", siwtches from 
class SwitchBackground(miniworldmaker.Token):
    def setup(self):
        self.add_costume("images/1")
        self.add_costume("images/2")
              
#token6 = SwitchBackground(position = (60,250))

# Token 7: Like 6, but switches to costume 1 (remember, counting from 0)
#token7 = SwitchBackground(position = (60,300))
#token7.switch_costume(1)

# Token 7 throws error because switching to costume 2 is not allowd
try:
    token7.switch_costume(2)
except Exception as e:
    print(e)

# Token 8: Purple in topleft corner (with center)
token8 = miniworldmaker.Token()
token8.size = (40,40)
token8.center=(200,0)


board.run()

