from pathlib import Path
from tkinter import Toplevel, Frame, Canvas, Button, PhotoImage
from gui.mainwindow.dashboard.gui import Dashboard
from gui.mainwindow.add_appointment.gui import AddAppointment
from gui.mainwindow.view_appointment.gui import ViewAppointment
from gui.mainwindow.inventory.gui import Inventory
from gui.mainwindow.about.gui import About
from gui.mainwindow.titles.dashboard_title import Dashboard_title
from gui.mainwindow.titles.appointment_title import Appointment_title
from gui.mainwindow.titles.inventory_title import Inventory_title
from gui.mainwindow.titles.about_title import About_title

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def mainWindow():
    MainWindow()

class MainWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.title("HappyTots - The state-of-art HMS")
        self.geometry("1012x506")
        self.configure(bg="#FFFFFF")
        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)

        self.canvas = Canvas(self, bg="#FFFFFF", height=506, width=1012, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(0, 0, 214, 506, fill="#F8DFCD", outline="")
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(107, 253, image=self.image_image_1)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.logout, relief="flat")
        self.button_1.place(x=25, y=475, width=109, height=24)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(105, 37, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.slider = self.canvas.create_image(2, 150, anchor="nw", image=self.image_image_3)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=lambda: self.animate_slider(150, "dashboard"), relief="flat")
        self.button_2.place(x=25, y=153, width=151, height=24)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0, command=lambda: self.animate_slider(189, "appointment"), relief="flat")
        self.button_3.place(x=25, y=192, width=175, height=24)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.button_4 = Button(self, image=self.button_image_4, borderwidth=0, highlightthickness=0, command=lambda: self.animate_slider(228, "inventory"), relief="flat")
        self.button_4.place(x=25, y=231, width=140, height=27)

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.button_5 = Button(self, image=self.button_image_5, borderwidth=0, highlightthickness=0, command=lambda: self.animate_slider(270, "about"), relief="flat")
        self.button_5.place(x=25, y=273, width=102, height=24)

        self.current_title = Frame(self, bg="white", width=798, height=74)
        self.current_title.place(x=214, y=0)

        self.content_frame = Frame(self, bg="white", width=797, height=432)
        self.content_frame.place(x=214, y=72)

        self.current_page = None
        self.current_slider_y = 150
        self.show_page("dashboard")

    def animate_slider(self, target_y, page_name):
        step = 5

        def move():
            nonlocal step
            current_y = self.canvas.coords(self.slider)[1]
            if abs(current_y - target_y) < step:
                self.canvas.coords(self.slider, 2, target_y)
                self.show_page(page_name)
            else:
                if current_y < target_y:
                    new_y = current_y + step
                else:
                    new_y = current_y - step
                self.canvas.coords(self.slider, 2, new_y)
                self.after(10, move)

        move()

    def show_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        for widget in self.current_title.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            self.current_page = Dashboard(self.content_frame)
            title = Dashboard_title(self.current_title)
        elif page_name == "appointment":
            self.current_page = AddAppointment(self.content_frame)
            title = Appointment_title(self.current_title)
        elif page_name == "view_appointment":
            self.current_page = ViewAppointment(self.content_frame)
            title = Appointment_title(self.current_title)
        elif page_name == "about":
            self.current_page = About(self.content_frame)
            title = About_title(self.current_title)
        elif page_name == "inventory":
            self.current_page = Inventory(self.content_frame)
            title = Inventory_title(self.current_title)

        self.current_page.place(x=0, y=0, relwidth=1, relheight=1)
        if title:
            title.place(x=0, y=0, relwidth=1, relheight=1)

        self.resizable(False, False)

    def logout(self):
        """Logout and return to login screen"""
        from gui.login.gui import login_window
        self.destroy()
        login_window()