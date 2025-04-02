from pathlib import Path
from tkinter import Toplevel, Canvas, Entry, Button, PhotoImage, messagebox, StringVar
import re
import threading

# Import the controller
from controller import signup_new_user

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def sign_up():
    SignUp(None)

class SignUp(Toplevel):
    def __init__(self, parent=None, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)

        self.title("Sign Up - Hospital Management System")
        self.geometry("600x400")
        self.configure(bg="#F9E6EE")
        
        # Center window on screen
        self.withdraw()
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.deiconify()

        self.canvas = Canvas(
            self,
            bg="#F9E6EE",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create StringVars for form fields
        self.email_var = StringVar()
        self.password_var = StringVar()
        self.confirm_password_var = StringVar()

        # Background images
        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(130.0, 200.0, image=self.image_1)

        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(432.0, 200.0, image=self.image_2)

        self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(380.0, 105.0, image=self.image_3)

        self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(379.0, 48.0, image=self.image_4)

        # Email entry
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(421.5, 170.0, image=self.entry_image_1)
        self.email_entry = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            textvariable=self.email_var
        )
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", self.on_entry_click)
        self.email_entry.bind("<FocusOut>", self.on_focusout)
        self.email_entry.place(x=291.0, y=147.0, width=261.0, height=44.0)

        # New password entry
        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(421.5, 229.0, image=self.entry_image_2)
        self.password_entry = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            textvariable=self.password_var
        )
        self.password_entry.insert(0, "New password")
        self.password_entry.bind("<FocusIn>", self.on_entry_click)
        self.password_entry.bind("<FocusOut>", self.on_focusout)
        self.password_entry.place(x=291.0, y=206.0, width=261.0, height=44.0)

        # Confirm password entry
        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.canvas.create_image(422.5, 288.0, image=self.entry_image_3)
        self.confirm_password_entry = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="grey",
            highlightthickness=0,
            textvariable=self.confirm_password_var
        )
        self.confirm_password_entry.insert(0, "Confirm password")
        self.confirm_password_entry.bind("<FocusIn>", self.on_entry_click)
        self.confirm_password_entry.bind("<FocusOut>", self.on_focusout)
        self.confirm_password_entry.place(x=292.0, y=265.0, width=261.0, height=44.0)

        # Sign Up button with hover effect
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.signup_button = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.signup_func,
            relief="flat",
            cursor="hand2",
            activebackground="#f0f0f0"
        )
        self.signup_button.place(x=312.0, y=333.0, width=222.0, height=41.0)
        self.signup_button.bind("<Enter>", lambda e: self.on_button_hover(self.signup_button))
        self.signup_button.bind("<Leave>", lambda e: self.on_button_leave(self.signup_button))

        # Additional images
        self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(434.0, 138.0, image=self.image_5)

        self.image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
        self.canvas.create_image(130.0, 200.0, image=self.image_6)

        self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
        self.canvas.create_image(160.0, 290.0, image=self.image_7)

        # Sign In button (overlaid on image_7) with hover effect
        self.signin_button = Button(
            self,
            text="",
            borderwidth=0,
            highlightthickness=0,
            command=self.show_login,
            relief="flat",
            bg="#F9E6EE",
            activebackground="#f0d6de",
            cursor="hand2"
        )
        self.signin_button.place(x=110.0, y=270.0, width=100.0, height=40.0)

        self.image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
        self.canvas.create_image(129.0, 179.0, image=self.image_8)
        
        # Privacy policy checkbox
        self.privacy_agreed = False
        self.privacy_checkbox = self.canvas.create_oval(292, 310, 300, 318, fill="white", outline="#000000")
        self.canvas.tag_bind(self.privacy_checkbox, "<Button-1>", lambda e: self.toggle_privacy_policy())
        
        self.privacy_text = self.canvas.create_text(
            305, 314, anchor="w",
            text="I agree to the Privacy Policy and Terms & Conditions",
            fill="#000000", font=("Inter SemiBold", 9 * -1)
        )
        self.canvas.tag_bind(self.privacy_text, "<Button-1>", lambda e: self.show_terms_and_conditions())
        
        # Bind Enter key to signup function
        self.bind("<Return>", lambda event: self.signup_func())

        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def signup_func(self):
        email = self.email_var.get().lower()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        # Validation checks
        if email in ["", "Email"]:
            messagebox.showerror("Error", "Please enter a valid email")
            return
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        if password in ["", "New password"]:
            messagebox.showerror("Error", "Please enter a password")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        if confirm_password in ["", "Confirm password"]:
            messagebox.showerror("Error", "Please confirm your password")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if not self.privacy_agreed:
            messagebox.showerror("Error", "Please agree to the Privacy Policy and Terms & Conditions")
            return

        # Import login_window here to avoid circular import
        from ..login.gui import login_window

        # Show loading indicator
        self.signup_button.config(state="disabled")
        self.update_idletasks()
        
        # Attempt to add user to database using controller in a separate thread
        threading.Thread(target=self.register_user, args=(email, password)).start()

    def register_user(self, email, password):
        try:
            if signup_new_user(email, password):
                self.after(0, lambda: self.signup_success(email))
            else:
                self.after(0, lambda: self.signup_error("Error", "Username already exists"))
        except Exception as e:
            self.after(0, lambda: self.signup_error("Database Error", f"Error: {str(e)}"))

    def signup_success(self, email):
        from ..login.gui import login_window
        messagebox.showinfo("Success", f"Account created successfully for {email}! Please login.")
        self.destroy()
        login_window()
        
    def signup_error(self, title, message):
        self.signup_button.config(state="normal")
        messagebox.showerror(title, message)

    def show_login(self):
        # Import login_window here to avoid circular import
        from ..login.gui import login_window
        self.destroy()
        login_window()

    def on_entry_click(self, event):
        if event.widget == self.email_entry and self.email_entry.get() == "Email":
            self.email_entry.delete(0, "end")
            self.email_entry.config(fg="black")
        elif event.widget == self.password_entry and self.password_entry.get() == "New password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="black", show="*")
        elif event.widget == self.confirm_password_entry and self.confirm_password_entry.get() == "Confirm password":
            self.confirm_password_entry.delete(0, "end")
            self.confirm_password_entry.config(fg="black", show="*")

    def on_focusout(self, event):
        if event.widget == self.email_entry and not self.email_entry.get():
            self.email_entry.insert(0, "Email")
            self.email_entry.config(fg="grey")
        elif event.widget == self.password_entry and not self.password_entry.get():
            self.password_entry.config(show="")
            self.password_entry.insert(0, "New password")
            self.password_entry.config(fg="grey")
        elif event.widget == self.confirm_password_entry and not self.confirm_password_entry.get():
            self.confirm_password_entry.config(show="")
            self.confirm_password_entry.insert(0, "Confirm password")
            self.confirm_password_entry.config(fg="grey")

    def on_button_hover(self, button):
        button.config(bg="#f5f5f5")
        
    def on_button_leave(self, button):
        button.config(bg="#FFFFFF")
        
    def toggle_privacy_policy(self):
        self.privacy_agreed = not self.privacy_agreed
        fill_color = "#4CAF50" if self.privacy_agreed else "white"
        self.canvas.itemconfig(self.privacy_checkbox, fill=fill_color)
    
    def show_terms_and_conditions(self):
        messagebox.showinfo(
            "Terms and Conditions",
            "Privacy Policy and Terms & Conditions\n\n"
            "1. This application collects user information for authentication purposes only.\n"
            "2. Patient data is stored securely and not shared with third parties.\n"
            "3. By using this system, you agree to handle patient information with confidentiality.\n"
            "4. The system is intended for authorized hospital staff only."
        )
    
    def is_valid_email(self, email):
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    sign_up()