import miniworldmaker

myboard = miniworldmaker.PhysicsBoard()
myboard.size = 400, 300
myboard.add_background((0,0,0,255))
token = miniworldmaker.Token((200,200))
token.size = (40, 40)
token.position = (10, 10)
token.add_costume((200,200,200,200))
myboard.run()