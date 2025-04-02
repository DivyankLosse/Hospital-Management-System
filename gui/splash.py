from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage
import time
import threading

# Import the login screen
from .login.gui import login_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./splash_assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class SplashScreen:
    def __init__(self, parent):
        # Create splash screen window
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("Hospital Management System")
        self.root.geometry("600x400")
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Center the splash screen
        self.center_window()
        
        # Create canvas
        self.canvas = Canvas(
            self.root,
            bg="#F8DFCD",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Gradient background
        for i in range(100):
            color = self.interpolate_color("#F8DFCD", "#FFFFFF", i/100)
            self.canvas.create_rectangle(0, i*4, 600, (i+1)*4, fill=color, outline="")
            
        # Create logo and text
        try:
            self.logo_image = PhotoImage(file=relative_to_assets("logo.png"))
            self.canvas.create_image(300, 140, image=self.logo_image)
        except:
            # If logo.png doesn't exist, create a text logo
            self.canvas.create_text(
                300, 140,
                text="HappyTots",
                fill="#333333",
                font=("Arial", 40, "bold")
            )
            
        # Title text
        self.canvas.create_text(
            300, 200,
            text="Hospital Management System",
            fill="#333333",
            font=("Arial", 18, "bold")
        )
        
        # Version and copyright
        self.canvas.create_text(
            300, 230,
            text="Version 1.0",
            fill="#666666",
            font=("Arial", 12)
        )
        
        self.canvas.create_text(
            300, 370,
            text="© Shruti, Uttkarsh & Divyank",
            fill="#666666",
            font=("Arial", 10)
        )
        
        # Progress bar background
        self.canvas.create_rectangle(100, 300, 500, 320, fill="#EEEEEE", outline="")
        
        # Progress bar 
        self.progress_rect = self.canvas.create_rectangle(100, 300, 100, 320, fill="#4CAF50", outline="")
        
        # Loading text
        self.loading_text = self.canvas.create_text(
            300, 340,
            text="Loading...",
            fill="#666666",
            font=("Arial", 10)
        )
        
        # Start progress animation
        self.progress = 0
        self.update_progress_bar()
        
        # Start timer to close splash and show login
        threading.Thread(target=self.simulate_loading).start()
        
    def center_window(self):
        # Get screen dimensions and center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")
        
    def interpolate_color(self, color1, color2, t):
        # Convert hex colors to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def update_progress_bar(self):
        if self.progress < 100:
            # Update progress bar position
            progress_width = int(400 * (self.progress / 100))
            self.canvas.coords(self.progress_rect, 100, 300, 100 + progress_width, 320)
            
            # Update loading text
            loading_stages = ["Loading system", "Connecting to database", "Initializing modules", "Preparing interface"]
            stage_index = int(self.progress / 25)
            if stage_index < len(loading_stages):
                self.canvas.itemconfig(self.loading_text, text=f"{loading_stages[stage_index]}...")
            
            self.root.after(30, self.update_progress_bar)
            
    def simulate_loading(self):
        # Simulate loading process
        for i in range(101):
            self.progress = i
            time.sleep(0.03)  # Adjust for desired splash screen duration
            
        # Ensure we're updating the UI from the main thread
        self.root.after(0, self.finish_splash)
            
    def finish_splash(self):
        # Close splash screen and show login window
        self.root.destroy()
        login_window()
        
def start_application():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Create splash screen
    splash = SplashScreen(root)
    
    # Start main loop
    root.mainloop()
    
if __name__ == "__main__":
    start_application() 