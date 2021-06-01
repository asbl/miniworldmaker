import os

import easygui

msg ="Choose Game"
title = "Ice Cream Survey"
choices = ["games/Angry Birds",
           "games/Asteroids",
           "games/Flappy Bird",
           "games/Pong",
           "games/Racing",
           "games/RPG",
           "gui/spinning_wheel",
           "gui/toolbar_rocket",
           "moving/bounce_from_token",
           "moving/flip_the_fish",
           "moving/follow_the_mouse",
           "moving/roboanimation",
           "moving/the_crash",
           ]
choice = easygui.choicebox(msg, title, choices)

if choice == "Angry Bird Example":
    os.chdir("games/angry")
    from games.angry import angry
    angry.main()
elif choice == "games/Asteroids":
    os.chdir("games/asteroids")
    from games.asteroids import asteroids
    asteroids.main()
elif choice == "games/Flappy":
    os.chdir("games/flappy")
    from games.flappy import flappy
    flappy.main()
elif choice == "games/Pong":
    os.chdir("games/pong")
    from games.flappy import pong
    pong.main()
elif choice == "games/Racing":
    os.chdir("games/racing")
    from games.racing import racing
    racing.main()
elif choice == "games/RPG":
    os.chdir("games/rpg")
    from games.rpg import rpg
    rpg.main()
elif choice == "gui/spinning_wheel":
    os.chdir("gui/")
    from gui.spinning_wheel import spinning_wheel
    spinning_wheel.main()
elif choice == "gui/":
    os.chdir("gui/")
    from gui.toolbar_rocket import toolbar_rocket
    toolbar_rocket.main()
elif choice == "moving/bounce_from_token":
    os.chdir("moving/")
    from moving.bounce_from_token import bounce_from_token
    bounce_from_token.main()
elif choice == "moving/flip_the_fish":
    os.chdir("moving/")
    from moving.flip_the_fish import flip_the_fish
    flip_the_fish.main()
elif choice == "moving/follow_the_mouse":
    os.chdir("moving/")
    from moving.follow_the_mouse import follow_the_mouse
    follow_the_mouse.main()
elif choice == "moving/move_on_tiled_board":
    os.chdir("moving/")
    from moving.move_on_tiled_board import move_on_tiled_board
    move_on_tiled_board.main()
elif choice == "moving/roboanmiation":
    os.chdir("moving/")
    from moving.roboanmiation import roboanmiation
    roboanmiation.main()
elif choice == "moving/the_crash":
    os.chdir("moving/")
    from moving.thecrash import thecrash
    thecrash.main()





