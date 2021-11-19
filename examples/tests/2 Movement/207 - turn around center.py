import miniworldmaker
board = miniworldmaker.PixelBoard(200,200)
board.add_background((0,0,0,255))
# Output should be a cross, not an inverted L!
tkn = miniworldmaker.Token()
tkn.position = (50,50)
tkn.add_costume((255,255,255,100))
tkn.size= (10, 100)
print("tkn1, position, center, ", tkn.position, tkn.center, tkn.rect, tkn.costume.image)


tkn2 = miniworldmaker.Token()
tkn2.position = (50,50)
tkn2.add_costume((0,255,255,100))
tkn2.size= (10, 100)
print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect)
tkn2.turn_left(90)
print("tkn2, position, center, ", tkn2.position, tkn2.center, tkn2.rect, tkn2.size, tkn2.rect)
board.run()

