from PIL import Image, ImageTk

# Load an animation set from files
def load_animation(folder, base_name, count):
    return [(ImageTk.PhotoImage(img), ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))) for img in [Image.open(f"{folder}/{base_name}_{i}.png") for i in range(1, count + 1)]] 

# Animate the player sprite based on the player's state
def animate_player(game):
    frame, delay = (game.animations["hurt"][game.current_frame % 2], 30) if game.hurt else \
                   (game.animations["jump"][0] if game.velocity_y < -15 else
                    game.animations["jump"][2] if game.velocity_y > 0 else
                    game.animations["jump"][1], 100) if game.jumping else \
                   (game.animations["walk"][game.current_frame % 6], 100) if game.moving else \
                   (game.animations["idle"][game.current_frame % 4], 200)

    game.canvas.itemconfig(game.player_image, image=frame[0 if game.direction == 1 else 1])
    game.current_frame += 1
    game.root.after(delay, animate_player, game)

# Animate the background
def animate_background(game):
    game.canvas.itemconfig(game.background_image, image=game.background_frames[game.background_frame % 8][0])
    game.background_frame += 1
    game.root.after(100, animate_background, game)
