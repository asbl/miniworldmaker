import miniworldmaker

myboard = miniworldmaker.PhysicsBoard()
myboard.size = 400, 300
myboard.add_background((0,0,0,255))
token = miniworldmaker.Token((200,200))
token.position = (100, 10)
token.add_costume((200,200,200,200))

token2 = miniworldmaker.Token((200,200))
token2.position = (100, 80)
token2.add_costume((200,200,200,200))
token2.set_simulation(None)
print(token2.physics._body.body_type)

token3 = miniworldmaker.Token((200,200))
token3.position = (100, 180)
token3.add_costume((200,200,200,200))
token3.set_simulation("manual")

token4 = miniworldmaker.Token((200,200))
token4.position = (150, 180)
token4.add_costume((200,200,200,200))
try:
    token4.set_simulation("other")
except Exception as e:
    print(e)
     

myboard.run()