import tkinter as tk
import time
from PIL import Image, ImageTk
from App.TitleScreen import TitleScreen
from App.Levels import level_data
from App.Controls import bind_controls
from App.Animations import load_animation, animate_player, animate_background
from App.Sounds import play_sound
from App.Enemy import Enemy
import math
import os
import platform

# Game Constants
WIDTH, HEIGHT = 640, 480
GAME_SPEED = 15
GRAVITY = 0.5
JUMP_STRENGTH, SPEED, VELOCITY = -10, 7, 0.85
HURT_KNOCKBACK, HURT_JUMP = 20, -8
ANIMATION_DELAY_IDLE = 200
ANIMATION_DELAY_WALK = 100
ANIMATION_DELAY_HURT = 30
RESET_HEIGHT = 600
ZOOM_SCALE = 1.5
MAX_LIVES = 5
HEART_SIZE = 40
TOTAL_LEVELS = 4

class PlatformerGame:
    def __init__(self, root, title_screen):
        self.root = root
        self.title_screen = title_screen
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.animations = {
            "idle": load_animation("Assets", "idle", 4),
            "walk": load_animation("Assets", "walk", 6),
            "jump": load_animation("Assets", "jump", 3),
            "hurt": load_animation("Assets", "hurt", 2)
        }

        self.background_frames = load_animation("Assets/Background", "background", 8)
        self.background_frame = 0

        heart_full_img = Image.open("Assets/heart_full.png")
        heart_empty_img = Image.open("Assets/heart_empty.png")
        heart_full_img = heart_full_img.resize((int(heart_full_img.width * HEART_SIZE / heart_full_img.height), HEART_SIZE), Image.Resampling.LANCZOS)
        heart_empty_img = heart_empty_img.resize((int(heart_empty_img.width * HEART_SIZE / heart_empty_img.height), HEART_SIZE), Image.Resampling.LANCZOS)
        self.heart_full = ImageTk.PhotoImage(heart_full_img)
        self.heart_empty = ImageTk.PhotoImage(heart_empty_img)

        # Timer variables
        self.start_time = None
        self.level_times = []  # Store times for each level

        # Timer display
        self.timer_label = tk.Label(root, text="Time: 0.00s", font=("Arial", 14), bg="lightgrey")
        self.timer_label.place(x=10, y=HEIGHT - 40)  # Bottom left corner

        self.level_label = tk.Label(root, text=f"Level: 1", font=("Arial", 16), bg="lightgrey")
        self.level_label.place(x=10, y=10)
        self.hearts = [tk.Label(root, image=self.heart_full, bg="lightgrey") for _ in range(MAX_LIVES)]
        for i, heart in enumerate(self.hearts):
            heart.place(x=WIDTH - (i + 1) * 42, y=10)

        self.lives = MAX_LIVES
        self.level = 1
        self.player_x, self.player_y = 100, 285
        self.velocity_x, self.velocity_y = 0, 0
        self.hurt = False
        self.invincible = False
        self.on_ground = False
        self.moving = False
        self.jumping = False
        self.enemies = []
        self.current_frame = 0
        self.direction = 1

        self.background_image = self.canvas.create_image(0, 0, image=self.background_frames[0][0], anchor="nw")
        self.player_image = self.canvas.create_image(self.player_x, self.player_y, image=self.animations["idle"][0][1], anchor="nw")
        self.canvas.tag_raise(self.player_image)

        self.load_level(self.level)
        bind_controls(self.root, self)
        animate_player(self)
        animate_background(self)
        self.update_game()

    def load_level(self, level):
        self.canvas.delete("all")
        self.level_label.config(text=f"Level: {level}")
        self.lives = MAX_LIVES
        for heart in self.hearts:
            heart.config(image=self.heart_full)
        self.enemies.clear()

        self.background_image = self.canvas.create_image(0, 0, image=self.background_frames[0][0], anchor="nw")
        self.player_image = self.canvas.create_image(self.player_x, self.player_y, image=self.animations["idle"][0][1], anchor="nw")
        self.canvas.tag_raise(self.player_image)

        level_design = level_data.get(level, [])
        self.platforms = []
        self.hurt_platform = None
        self.level_platform = None
        for platform in level_design:
            if platform[0] == "hurt":
                self.hurt_platform = self.canvas.create_rectangle(*platform[1:], fill="#1e2145")
            elif platform[0] == "level":
                self.level_platform = self.canvas.create_rectangle(*platform[1:], fill="#ab8827")
            elif platform[0] == "enemy":
                if len(platform) > 6:
                    enemy = Enemy(self.canvas, *platform[1:6], platform[6])
                else:
                    enemy = Enemy(self.canvas, *platform[1:])
                self.enemies.append(enemy)
            else:
                self.platforms.append(self.canvas.create_rectangle(*platform, fill="#5e7568"))
        # Start timer for the new level
        self.start_time = time.time()

    def move(self, direction):
        if not self.hurt and not self.invincible:
            self.direction, self.velocity_x, self.moving = direction, SPEED * direction, True

    def stop(self):
        self.moving = False

    def jump(self, event=None):
        if self.on_ground and not self.hurt:
            self.velocity_y, self.jumping = JUMP_STRENGTH, True
            play_sound("jump.wav")

    def check_collision(self):
        self.on_ground = False
        for platform in self.platforms:
            x1, y1, x2, y2 = self.canvas.coords(platform)

            # Top collision (landing on platform)
            if self.player_x + 45 > x1 and self.player_x + 35 < x2 and y1 - 5 <= self.player_y + 50 <= y1 + 5 and self.velocity_y >= 0:
                self.on_ground = True
                self.velocity_y = 0
                self.player_y = y1 - 50
                self.jumping = False
                self.hurt = False
                self.invincible = False

            # Left collision (hitting right side of platform)
            elif self.player_x + 45 > x1 and self.player_x + 45 < x1 + 10 and y1 < self.player_y + 50 and y2 > self.player_y:
                self.velocity_x = 0
                self.player_x = x1 - 45

            # Right collision (hitting left side of platform)
            elif self.player_x + 35 < x2 and self.player_x + 35 > x2 - 10 and y1 < self.player_y + 50 and y2 > self.player_y:
                self.velocity_x = 0
                self.player_x = x2 - 35

            if self.lives <= 0:
                self.reset_game()

    def check_hurt_platform(self):
        if self.hurt_platform:
            x1, y1, x2, y2 = self.canvas.coords(self.hurt_platform)
            if x1 < self.player_x + 45 and x2 > self.player_x + 35 and y1 < self.player_y + 50 and y2 > self.player_y:
                self.hurt_player()

    def check_level_platform(self):
        if self.level_platform:
            x1, y1, x2, y2 = self.canvas.coords(self.level_platform)
            if x1 < self.player_x + 45 and x2 > self.player_x + 35 and y1 < self.player_y + 60 and y2 > self.player_y:
                self.complete_level()
                self.player_x, self.player_y = 100, 285  # Reset player position
                self.velocity_x, self.velocity_y = 0, 0  # Reset movement
                
    def complete_level(self):
        """Save level time and move to next level or end the game."""
        if self.start_time:
            level_time = round(time.time() - self.start_time, 2)  # Calculate time elapsed
            self.level_times.append(level_time)  # Store time

        if self.level < TOTAL_LEVELS:
            self.level += 1
            self.load_level(self.level)
        else:
            self.show_completion_screen()  # End game after Level 4

    def show_completion_screen(self):
        """Show a summary screen with level times and total time."""
        total_time = sum(self.level_times)
        
        self.canvas.delete("all")  # Clear the game screen
        self.timer_label.place_forget()  # Hide timer
        self.level_label.place_forget()  # Hide level label
        
        summary_text = "Game Complete!\n\nLevel Times:\n"
        for i, time_taken in enumerate(self.level_times, 1):
            summary_text += f"Level {i}: {time_taken} seconds\n"
        summary_text += f"\nTotal Time: {total_time} seconds"

        summary_label = tk.Label(self.root, text=summary_text, font=("Arial", 16), bg="white", fg="black", justify="left")
        summary_label.place(x=WIDTH//2 - 100, y=HEIGHT//2 - 50)

    def check_enemy_collision(self):
        for enemy in self.enemies:
            x1, y1 = self.canvas.coords(enemy.enemy_image)
            x2 = x1 + enemy.width
            y2 = y1 + enemy.height
            if (x1 < self.player_x + 45 and 
                x2 > self.player_x + 35 and 
                y1 < self.player_y + 50 and 
                y2 > self.player_y):
                self.hurt_player()

    def hurt_player(self):
        if not self.invincible:
            self.hurt, self.velocity_x, self.velocity_y = True, -self.direction * HURT_KNOCKBACK, HURT_JUMP
            self.lives -= 1
            self.invincible = True
            self.update_hearts()
            play_sound("hurt.wav")
            if self.lives <= 0:
                self.reset_game()

    def update_hearts(self):
        for i, heart in enumerate(self.hearts):
            if i < self.lives:
                heart.config(image=self.heart_full)
            else:
                heart.config(image=self.heart_empty)

    def update_game(self):
        self.velocity_y += GRAVITY
        self.player_y += self.velocity_y
        self.velocity_x = SPEED * self.direction if self.moving and not self.hurt else self.velocity_x * VELOCITY
        if abs(self.velocity_x) < 0.5: self.velocity_x = 0
        self.player_x += self.velocity_x

        self.check_collision()
        self.check_hurt_platform()
        self.check_level_platform()
        self.check_enemy_collision()

        for enemy in self.enemies:
            enemy.move()
        if self.player_y > RESET_HEIGHT:
            self.hurt_player()
            self.player_x, self.player_y, self.velocity_x, self.velocity_y, self.moving, self.jumping, self.hurt = 100, 285, 0, 0, False, False, False

        if self.start_time:
            elapsed_time = round(time.time() - self.start_time, 2)  # Calculate elapsed time
            self.timer_label.config(text=f"Time: {elapsed_time}s")  # Update label
            
        self.update_camera()
        self.canvas.coords(self.player_image, self.player_x, self.player_y - 25)
        self.root.after(GAME_SPEED, self.update_game)

    def update_camera(self):
        self.canvas.config(scrollregion=(0, 0, WIDTH * ZOOM_SCALE, HEIGHT * ZOOM_SCALE))
        self.canvas.xview_moveto((self.player_x - WIDTH / (2 * ZOOM_SCALE)) / (WIDTH * ZOOM_SCALE))
        
    def reset_game(self):
        self.lives = MAX_LIVES
        self.level = 1
        self.player_x, self.player_y = 100, 285
        self.velocity_x, self.velocity_y = 0, 0
        self.hurt = False
        self.invincible = False
        self.on_ground = False
        self.moving = False
        self.jumping = False
        self.direction = 1
        self.load_level(self.level)

if __name__ == "__main__":
    root = tk.Tk()
    title_screen = TitleScreen(root, WIDTH, HEIGHT)
    title_screen.show()
    root.mainloop()
