from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Project\Hospital main final\gui\mainwindow\titles\dashboard")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def dashboard_title():
    Dashboard_title

class Dashboard_title(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # Use super() for cleaner inheritance
        self.configure(bg="#F9E6EE")

        self.canvas = Canvas(
            self,
            bg="#F9E6EE",
            height=60,
            width=798,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Store images in instance variables to prevent garbage collection
        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))

        # Place images on the canvas
        self.canvas.create_image(81.0, 30.0, image=self.image_1)
        self.canvas.create_image(770.0, 29.0, image=self.image_2)
        self.canvas.create_image(372.0, 54.0, image=self.image_3)  # Fixed floating-point
        self.canvas.create_image(399.0, 30.0, image=self.image_4)

        # Admin Label
        self.canvas.create_text(
            686.0,
            22.0,
            anchor="nw",
            text="Admin",
            fill="#716F6F",
            font=("Montserrat Bold", 15 * -1)
        )
