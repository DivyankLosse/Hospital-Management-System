from pathlib import Path
from tkinter import Toplevel, Canvas, Entry, Button, PhotoImage, messagebox, StringVar
import webbrowser
import threading
import re

# Import the controller
from controller import check_user

# Import mainWindow
from ..mainwindow.gui import mainWindow

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def login_window():
    Login()

class Login(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Login - Hospital Management System")
        self.geometry("1012x506")
        self.configure(bg="#FFFFFF")
        
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
            bg="#FFFFFF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background images and layout
        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(506.0, 253.0, image=image_image_1)

        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(291.0, 253.0, image=image_image_2)

        image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(163.0, 56.0, image=image_image_3)

        self.canvas.create_text(
            32.0, 113.0, anchor="nw",
            text=" Welcome.... To HappyTots!\nYour trusted Hospital Management \nSystem for managing patients,\nappointments and registrations \nseamlessly. Log in now to \n    explore!",
            fill="#FFFFFF", font=("Just Me Again Down Here", 32 * -1)
        )

        self.canvas.create_text(
            12.0, 452.0, anchor="nw",
            text="© Shruti, Uttkarsh & Divyank",
            fill="#FFFFFF", font=("Montserrat Bold", 18 * -1)
        )

        self.canvas.create_text(
            710.0, 37.0, anchor="nw",
            text="Enter your login details",
            fill="#000000", font=("Inder Regular", 20 * -1)
        )

        # Create StringVars for entry fields for validation
        self.email_var = StringVar()
        self.password_var = StringVar()

        # Social login buttons with hover effect
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.google_button = Button(
            self.canvas, 
            image=self.button_image_1, 
            command=self.google_login, 
            relief="flat", 
            bg="white",
            borderwidth=0,
            activebackground="#f0f0f0",
            cursor="hand2"
        )
        self.google_button.place(x=706, y=132, width=232, height=46)
        self.google_button.bind("<Enter>", lambda e: self.on_button_hover(self.google_button))
        self.google_button.bind("<Leave>", lambda e: self.on_button_leave(self.google_button))

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.apple_button = Button(
            self.canvas, 
            image=self.button_image_2, 
            command=self.apple_login, 
            relief="flat", 
            bg="white",
            borderwidth=0,
            activebackground="#f0f0f0",
            cursor="hand2"
        )
        self.apple_button.place(x=706, y=186, width=232, height=46)
        self.apple_button.bind("<Enter>", lambda e: self.on_button_hover(self.apple_button))
        self.apple_button.bind("<Leave>", lambda e: self.on_button_leave(self.apple_button))

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.facebook_button = Button(
            self.canvas, 
            image=self.button_image_4, 
            command=self.facebook_login, 
            relief="flat", 
            bg="white",
            borderwidth=0,
            activebackground="#f0f0f0",
            cursor="hand2"
        )
        self.facebook_button.place(x=706, y=78, width=232, height=46)
        self.facebook_button.bind("<Enter>", lambda e: self.on_button_hover(self.facebook_button))
        self.facebook_button.bind("<Leave>", lambda e: self.on_button_leave(self.facebook_button))

        # Email entry
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(821.5, 274.8, image=self.entry_image_1)
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
        self.email_entry.place(x=720.0, y=254.8, width=203.0, height=38.0)

        # Password entry
        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(821.5, 329.8, image=self.entry_image_2)
        self.password_entry = Entry(
            self, 
            bd=0, 
            bg="#FFFFFF", 
            fg="grey", 
            highlightthickness=0,
            textvariable=self.password_var
        )
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.on_entry_click)
        self.password_entry.bind("<FocusOut>", self.on_focusout)
        self.password_entry.place(x=720.0, y=309.8, width=203.0, height=38.0)

        # Login button with hover effect
        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.login_button = Button(
            self.canvas, 
            image=button_image_3, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.login_func, 
            relief="flat",
            cursor="hand2",
            activebackground="#f0f0f0"
        )
        self.login_button.place(x=713, y=372, width=218, height=44)
        self.login_button.bind("<Enter>", lambda e: self.on_button_hover(self.login_button))
        self.login_button.bind("<Leave>", lambda e: self.on_button_leave(self.login_button))

        # Privacy policy checkbox
        self.privacy_agreed = False
        button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.privacy_button = Button(
            self.canvas, 
            image=button_image_5, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.toggle_privacy_policy, 
            relief="flat",
            cursor="hand2"
        )
        self.privacy_button.place(x=733.0, y=460.0, width=8.0, height=8.0)

        self.privacy_text = self.canvas.create_text(
            743.0, 460.0, anchor="nw",
            text="Read and agreed to Privacy Policy and T&C",
            fill="#000000", font=("Inter SemiBold", 7 * -1)
        )
        
        # Make privacy text clickable to show T&C
        self.canvas.tag_bind(self.privacy_text, "<Button-1>", lambda e: self.show_terms_and_conditions())

        # Sign up link with hover effect
        image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(796.0, 433.0, image=image_image_4)

        button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        self.signup_button = Button(
            self.canvas, 
            image=button_image_6, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.show_signup, 
            relief="flat",
            cursor="hand2"
        )
        self.signup_button.place(x=836.0, y=424.0, width=64.0, height=14.0)
        
        # Bind Enter key to login function
        self.bind("<Return>", lambda event: self.login_func())

        # Store all PhotoImage references to prevent garbage collection
        self.images = {
            "image_1": image_image_1,
            "image_2": image_image_2,
            "image_3": image_image_3,
            "image_4": image_image_4,
            "button_3": button_image_3,
            "button_5": button_image_5,
            "button_6": button_image_6
        }

        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def login_func(self):
        username = self.email_var.get().lower()
        password = self.password_var.get()
        
        if username == "Email" or password == "Password" or not username or not password:
            messagebox.showerror("Error", "Please enter valid credentials")
            return
            
        if not self.privacy_agreed:
            messagebox.showerror("Error", "Please agree to the Privacy Policy and Terms & Conditions")
            return
            
        # Email validation
        if not self.is_valid_email(username):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        # Show loading indicator
        self.login_button.config(state="disabled")
        self.update_idletasks()
        
        try:
            # Run authentication in a separate thread
            threading.Thread(target=self.authenticate, args=(username, password)).start()
        except Exception as e:
            self.login_button.config(state="normal")
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")

    def authenticate(self, username, password):
        try:
            if check_user(username, password):
                # Use after() to ensure thread-safe UI updates
                self.after(0, self.login_success)
            else:
                self.after(0, lambda: self.login_error("Invalid Credentials", "The username and password don't match"))
        except Exception as e:
            self.after(0, lambda: self.login_error("Database Error", f"Error connecting to database: {str(e)}"))

    def login_success(self):
        self.destroy()
        mainWindow()

    def login_error(self, title, message):
        self.login_button.config(state="normal")
        messagebox.showerror(title=title, message=message)

    def google_login(self):
        try:
            webbrowser.open("http://127.0.0.1:5000/login/google")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Google login: {str(e)}")

    def apple_login(self):
        try:
            webbrowser.open("https://appleid.apple.com/auth/authorize?client_id=YOUR_APPLE_CLIENT_ID&redirect_uri=http://127.0.0.1:5000/callback/apple")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Apple login: {str(e)}")

    def facebook_login(self):
        try:
            webbrowser.open("https://www.facebook.com/v14.0/dialog/oauth?client_id=YOUR_FACEBOOK_CLIENT_ID&redirect_uri=http://127.0.0.1:5000/callback/facebook")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Facebook login: {str(e)}")

    def show_signup(self):
        # Import sign_up here to avoid circular import
        from ..sign_up.gui import sign_up
        self.destroy()
        sign_up()

    def on_entry_click(self, event):
        if event.widget == self.email_entry and self.email_entry.get() == "Email":
            self.email_entry.delete(0, "end")
            self.email_entry.config(fg="black")
        elif event.widget == self.password_entry and self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="black", show="*")

    def on_focusout(self, event):
        if event.widget == self.email_entry and not self.email_entry.get():
            self.email_entry.insert(0, "Email")
            self.email_entry.config(fg="grey")
        elif event.widget == self.password_entry and not self.password_entry.get():
            self.password_entry.config(show="")
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="grey")

    def on_button_hover(self, button):
        button.config(bg="#f5f5f5")
        
    def on_button_leave(self, button):
        button.config(bg="white")
        
    def toggle_privacy_policy(self):
        self.privacy_agreed = not self.privacy_agreed
        if self.privacy_agreed:
            self.privacy_button.config(bg="#4CAF50")
        else:
            self.privacy_button.config(bg="white")
    
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
    login_window()