import miniworldmaker
board = miniworldmaker.PixelBoard(600,400)
board.add_background((200,0,0,255))
board.toolbar = board.add_container(miniworldmaker.InspectActorToolbar(board),
                                    "right")
tkn = miniworldmaker.Token()
tkn.position = (50,50)
tkn.add_costume((255,255,255,255))
tkn.size= (80, 80)

board.run()


