import tkinter as tk
from App.Controls import start_controls

class TitleScreen:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.root.title("Red Riding Hood Platformer")

        start_controls(self.root, self)
        
        # Create canvas for the title screen
        self.canvas = tk.Canvas(root, width=width, height=height, bg="lightblue")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add title text
        self.title_text = self.canvas.create_text(width // 2, height // 3, text="Red Riding Hood Platformer", font=("Arial", 30, "bold"), fill="black")
        
        # Add start button
        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 16), command=self.start_game)
        self.start_button.pack(pady=height // 2, anchor='center')

        # Initially, the title screen is visible and the button is enabled
        self.is_title_screen = True

        # Update button position dynamically when the window is resized
        self.root.bind("<Configure>", self.update_button_position)

    def start_game(self):
        if not self.is_title_screen:
            return  # Do nothing if we're not on the title screen
        
        # Disable the button during the game
        self.is_title_screen = False
        self.start_button.config(state=tk.DISABLED)

        # Hide the title screen and start the game
        self.hide()

        # Import PlatformerGame here to avoid circular import
        from Platformer import PlatformerGame
        game = PlatformerGame(self.root, self)  # Pass the TitleScreen reference to the game

    def show(self):
        """Show the title screen and the start button."""
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.start_button.pack(pady=self.height // 2, anchor='center')

        # Re-enable the start button if it's disabled
        if not self.is_title_screen:
            self.is_title_screen = True
            self.start_button.config(state=tk.NORMAL)

    def hide(self):
        """Hide the title screen and start button."""
        self.canvas.pack_forget()
        self.start_button.pack_forget()

    def update_button_position(self, event):
        """Update the position of the start button when the window size changes."""
        if self.root.winfo_width() != self.width or self.root.winfo_height() != self.height:
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            self.start_button.place(x=self.width // 2 - 75, y=self.height // 2)
