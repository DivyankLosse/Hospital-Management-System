from pathlib import Path
from tkinter import Frame, Canvas, Entry, Button, PhotoImage, messagebox
from gui.mainwindow.view_appointment.gui import ViewAppointment
from gui.mainwindow.titles.appointment_title import Appointment_title
from controller import add_patient_appointment

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def add_appointment():
    AddAppointment()

class AddAppointment(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg="#F9E6EE")

        self.canvas = Canvas(self, bg="#F9E6EE", height=432, width=797, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(399.0, 216.0, image=self.image_1)

        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(536.0, 217.99447631835938, image=self.image_2)

        self.canvas.create_text(164.0, 28.0, anchor="nw", text="Add Appointment", fill="#867264", font=("Montserrat Bold", 24 * -1))
        self.canvas.create_text(598.0, 27.0, anchor="nw", text="Operations", fill="#867264", font=("Montserrat Bold", 24 * -1))

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(99.5, 194.0, image=self.entry_image_1)
        self.entry_1 = Entry(self, bd=0, bg="#DFD9D6", fg="#000716", font=("Montserrat Bold", 16 * -1), highlightthickness=0)
        self.entry_1.insert(0, "Age")
        self.entry_1.bind("<FocusIn>", self.on_entry_click)
        self.entry_1.bind("<FocusOut>", self.on_focusout)
        self.entry_1.place(x=54.0, y=163.0, width=91.0, height=60.0)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(144.5, 105.0, image=self.entry_image_2)
        self.entry_2 = Entry(self, bd=0, bg="#DFD9D6", fg="#000716", font=("Montserrat Bold", 16 * -1), highlightthickness=0)
        self.entry_2.insert(0, "Name")
        self.entry_2.bind("<FocusIn>", self.on_entry_click)
        self.entry_2.bind("<FocusOut>", self.on_focusout)
        self.entry_2.place(x=54.0, y=74.0, width=181.0, height=60.0)

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.canvas.create_image(398.5, 105.0, image=self.entry_image_3)
        self.entry_3 = Entry(self, bd=0, bg="#DFD9D6", fg="#000716", font=("Montserrat Bold", 16 * -1), highlightthickness=0)
        self.entry_3.insert(0, "Phone No")
        self.entry_3.bind("<FocusIn>", self.on_entry_click)
        self.entry_3.bind("<FocusOut>", self.on_focusout)
        self.entry_3.place(x=308.0, y=74.0, width=181.0, height=60.0)

        self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        self.canvas.create_image(271.5, 283.0, image=self.entry_image_4)
        self.entry_4 = Entry(self, bd=0, bg="#DFD9D6", fg="#000716", font=("Montserrat Bold", 16 * -1), highlightthickness=0)
        self.entry_4.insert(0, "Address")
        self.entry_4.bind("<FocusIn>", self.on_entry_click)
        self.entry_4.bind("<FocusOut>", self.on_focusout)
        self.entry_4.place(x=54.0, y=252.0, width=435.0, height=60.0)

        self.entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
        self.canvas.create_image(353.5, 194.0, image=self.entry_image_5)
        self.entry_5 = Entry(self, bd=0, bg="#DFD9D6", fg="#000716", font=("Montserrat Bold", 16 * -1), highlightthickness=0)
        self.entry_5.insert(0, "Gender")
        self.entry_5.bind("<FocusIn>", self.on_entry_click)
        self.entry_5.bind("<FocusOut>", self.on_focusout)
        self.entry_5.place(x=308.0, y=163.0, width=91.0, height=60.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=lambda: self.show_page("view"), relief="flat")
        self.button_1.place(x=543.0, y=118.0, width=248.0, height=68.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=lambda: self.show_page("view"), relief="flat")
        self.button_2.place(x=543.0, y=260.0, width=248.0, height=68.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = Button(self, image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.save_appointment, relief="flat")
        self.button_3.place(x=211.0, y=358.0, width=137.0, height=44.0)

    def save_appointment(self):
        name = self.entry_2.get()
        phone = self.entry_3.get()
        address = self.entry_4.get()
        gender = self.entry_5.get()
        age = self.entry_1.get()
        if all([name, phone, gender, age]) and name != "Name" and phone != "Phone No" and gender != "Gender" and age != "Age":
            try:
                appointment_id = add_patient_appointment(name, phone, address, gender, int(age))
                messagebox.showinfo("Success", f"Appointment added with ID: {appointment_id}")
                self.show_page("view")
            except ValueError:
                messagebox.showerror("Error", "Age must be a number")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add appointment: {e}")
        else:
            messagebox.showerror("Error", "Please fill all required fields")

    def show_page(self, page_name):
        if page_name == "view":
            for widget in self.winfo_children():
                widget.destroy()
            self.current_page = ViewAppointment(self)
            self.current_page.place(x=0, y=0, relwidth=1, relheight=1)

    def on_entry_click(self, event):
        if event.widget == self.entry_5 and self.entry_5.get() == "Gender":
            self.entry_5.delete(0, "end")
            self.entry_5.config(fg="black")
        elif event.widget == self.entry_1 and self.entry_1.get() == "Age":
            self.entry_1.delete(0, "end")
            self.entry_1.config(fg="black")
        elif event.widget == self.entry_2 and self.entry_2.get() == "Name":
            self.entry_2.delete(0, "end")
            self.entry_2.config(fg="black")
        elif event.widget == self.entry_3 and self.entry_3.get() == "Phone No":
            self.entry_3.delete(0, "end")
            self.entry_3.config(fg="black")
        elif event.widget == self.entry_4 and self.entry_4.get() == "Address":
            self.entry_4.delete(0, "end")
            self.entry_4.config(fg="black")

    def on_focusout(self, event):
        if event.widget == self.entry_5 and not self.entry_5.get():
            self.entry_5.insert(0, "Gender")
            self.entry_5.config(fg="grey")
        elif event.widget == self.entry_1 and not self.entry_1.get():
            self.entry_1.insert(0, "Age")
            self.entry_1.config(fg="grey")
        elif event.widget == self.entry_2 and not self.entry_2.get():
            self.entry_2.insert(0, "Name")
            self.entry_2.config(fg="grey")
        elif event.widget == self.entry_3 and not self.entry_3.get():
            self.entry_3.insert(0, "Phone No")
            self.entry_3.config(fg="grey")
        elif event.widget == self.entry_4 and not self.entry_4.get():
            self.entry_4.insert(0, "Address")
            self.entry_4.config(fg="grey")