from PIL import Image, ImageTk
import math

# Game Constants (needed for Enemy class)
PATROL_DISTANCE = 100
WOLF_ANIMATION_DELAY = 150

class Enemy:
    def __init__(self, canvas, x, y, width, height, speed, enemy_type="bat"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = 1  # Start moving right
        self.current_frame = 0
        self.animation_direction = 1
        self.enemy_type = enemy_type
        
        # Bat-specific attributes
        self.bob_amplitude = 3
        self.bob_speed = 0.05
        self.bob_offset = 0
        
        # Wolf-specific attributes
        self.start_x = x
        self.patrol_distance = PATROL_DISTANCE

        # Load appropriate frames based on enemy type
        if enemy_type == "bat":
            self.frames = []
            for i in range(1, 7):
                img = Image.open(f"Assets/bat_{i}.png")
                self.frames.append({
                    'right': ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)),
                    'left': ImageTk.PhotoImage(img)
                })
                if i == 1:
                    self.width = img.width
                    self.height = img.height
            self.max_frame = 5
        elif enemy_type == "wolf":
            self.frames = []
            for i in range(1, 4):  # 3 frames for wolf
                img = Image.open(f"Assets/wolf_{i}.png")
                self.frames.append({
                    'right': ImageTk.PhotoImage(img),  # Right is now the original image
                    'left': ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT))  # Left is flipped
                })
                if i == 1:
                    self.width = img.width
                    self.height = img.height
            self.max_frame = 2
        
        # Start with right-facing sprite
        self.enemy_image = self.canvas.create_image(self.x, self.y, image=self.frames[0]['right'], anchor="nw")
        self.animate()

    def move(self):
        if self.enemy_type == "bat":
            self.x += self.speed * self.direction
            if self.x < 0 or self.x + self.width > 980:
                self.direction *= -1
            self.bob_offset += self.bob_speed
            self.y += self.bob_amplitude * math.sin(self.bob_offset)
        elif self.enemy_type == "wolf":
            self.x += self.speed * self.direction
            # Reverse direction if wolf exceeds patrol distance from starting position
            if self.x > self.start_x + self.patrol_distance or self.x < self.start_x - self.patrol_distance:
                self.direction *= -1
        
        self.canvas.coords(self.enemy_image, self.x, self.y)

    def animate(self):
        self.current_frame += self.animation_direction
        if self.current_frame >= self.max_frame:
            self.animation_direction = -1
        elif self.current_frame <= 0:
            self.animation_direction = 1
        direction_key = 'right' if self.direction > 0 else 'left'
        self.canvas.itemconfig(self.enemy_image, image=self.frames[self.current_frame][direction_key])
        
        # Use different animation delay based on enemy type
        delay = 60 if self.enemy_type == "bat" else WOLF_ANIMATION_DELAY
        self.canvas.after(delay, self.animate)
