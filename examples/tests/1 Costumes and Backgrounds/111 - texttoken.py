import miniworldmaker
board = miniworldmaker.PixelBoard((200,200))
board.add_background((0,0,0,255))

token = miniworldmaker.TextToken((0,0), "Hello World!")
token.auto_size = "font"

token2 = miniworldmaker.TextToken((0,60))
token2.set_text("Hello!")
token2.auto_size = "token"
token2.font_size = 32

token3 = miniworldmaker.NumberToken((0,150))
token3.auto_size = None
token3.font_size=64

board.run()