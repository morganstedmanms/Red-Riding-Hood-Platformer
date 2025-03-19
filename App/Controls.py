def bind_controls(root, game):

    # Arrow Keys
    root.bind("<Left>", lambda e: game.move(-1))
    root.bind("<Right>", lambda e: game.move(1))
    root.bind("<Up>", game.jump)
    root.bind("<space>", game.jump)
    root.bind("<KeyRelease-Left>", lambda e: game.stop())
    root.bind("<KeyRelease-Right>", lambda e: game.stop())
    
    # WASD Keys
    root.bind("<a>", lambda e: game.move(-1))  # 'a' for left
    root.bind("<d>", lambda e: game.move(1))   # 'd' for right
    root.bind("<w>", game.jump)                 # 'w' for jump
    root.bind("<space>", game.jump)             # 'space' for jump
    root.bind("<KeyRelease-a>", lambda e: game.stop())  # Release 'a' to stop
    root.bind("<KeyRelease-d>", lambda e: game.stop())  # Release 'd' to stop

def start_controls(root, game):
    root.bind("<Return>", lambda event: game.start_game())
    root.bind("<space>", lambda event: game.start_game())