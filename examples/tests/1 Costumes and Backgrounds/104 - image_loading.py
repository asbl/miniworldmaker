import miniworldmaker

board = miniworldmaker.PixelBoard(400,300)
board.add_background("images/stone")

token1 = miniworldmaker.Token()
token1.add_costume("images/player")
token1.position = (20,20)
try:
    token2 = miniworldmaker.Token()
    token2.position = (120,120)
    token2.add_costume("images/player.gif")
except Exception as e:
    print(e)
board.run()