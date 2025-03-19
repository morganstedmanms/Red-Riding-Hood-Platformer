import tkinter as tk

class PlatformDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Platform Drawer")
        
        self.canvas = tk.Canvas(root, width=980, height=480, bg="white")
        self.canvas.pack()
        
        self.platforms = []  # List to store platform coordinates
        self.start_x = None
        self.start_y = None
        
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        
    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y

    def drawing(self, event):
        self.canvas.delete("preview")
        self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", tags="preview")
    
    def end_draw(self, event):
        end_x, end_y = event.x, event.y
        
        # Ensure proper ordering of coordinates
        x1, y1, x2, y2 = min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y)
        
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="gray")
        self.platforms.append((x1, y1, x2, y2))
        print(f"Platform: ({x1}, {y1}, {x2}, {y2})")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PlatformDrawer(root)
    root.mainloop()
