from pathlib import Path
from tkinter import Frame, Canvas, Entry, Button, PhotoImage, messagebox, Scrollbar, VERTICAL
from controller import get_all_appointments, update_appointment_status, delete_appointment, get_appointment_details

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def view_appointment():
    ViewAppointment()

class ViewAppointment(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg="#F9E6EE")
        
        # Store selected appointment ID
        self.selected_appointment_id = None

        # Create canvas with scrollbar
        self.canvas = Canvas(self, bg="#F9E6EE", height=432, width=797, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Add scrollbar to canvas
        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=780, y=101, height=228)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Set up the scrollable area
        self.scrollable_frame = Frame(self.canvas, bg="#EFEFEF")
        self.scrollable_frame_window = self.canvas.create_window((41, 102), window=self.scrollable_frame, anchor="nw", width=700, height=227)
        
        # Configure canvas scrolling
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(398.0, 216.0, image=self.image_1)

        self.canvas.create_rectangle(40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline="")
        self.canvas.create_rectangle(40.0, 342.0, 742.0, 344.0, fill="#EFEFEF", outline="")

        self.canvas.create_text(116.0, 33.0, anchor="nw", text="View Appointment", fill="#867264", font=("Montserrat Bold", 26 * -1))
        self.canvas.create_text(40.0, 367.0, anchor="nw", text="Avail. Actions:", fill="#867264", font=("Montserrat Bold", 26 * -1))
        self.canvas.create_text(116.0, 65.0, anchor="nw", text="And Perform Operations", fill="#808080", font=("Montserrat SemiBold", 16 * -1))

        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(666.0, 59.0, image=self.image_2)

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(680.5, 60.0, image=entry_image_1)
        self.entry_1 = Entry(self, bd=0, bg="#EFEFEF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=637.0, y=48.0, width=87.0, height=22.0)
        self.entry_1.bind("<Return>", lambda event: self.search_appointments())

        self.canvas.create_text(639.0, 50.0, anchor="nw", text="Search...", fill="#000000", font=("Montserrat SemiBold", 17 * -1))

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(self, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.refresh_appointments, relief="flat")
        self.button_1.place(x=525.0, y=33.0, width=53.0, height=53.0)

        self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(617.0, 60.0, image=self.image_3)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(self, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.search_appointments, relief="flat")
        self.button_2.place(x=40.0, y=33.0, width=53.0, height=53.0)

        # Update button text for better clarity
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self, 
            image=self.button_image_3, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.delete_selected_appointment, 
            relief="flat"
        )
        self.button_3.place(x=596.0, y=359.0, width=146.0, height=48.0)

        # Change text to "Approve"
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self, 
            image=self.button_image_4, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.approve_selected_appointment, 
            relief="flat"
        )
        self.button_4.place(x=463.0, y=359.0, width=116.0, height=48.0)

        self.canvas.create_rectangle(40.0, 101.0, 742.0, 329.0, fill="#EFEFEF", outline="")

        # Change text to "View Details"
        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            self, 
            image=self.button_image_5, 
            borderwidth=0, 
            highlightthickness=0, 
            command=self.view_appointment_details, 
            relief="flat"
        )
        self.button_5.place(x=272.0, y=359.0, width=174.0, height=48.0)
        
        # Add column headers
        self.canvas.create_text(50, 110, anchor="nw", text="ID", fill="#333333", font=("Montserrat Bold", 12))
        self.canvas.create_text(100, 110, anchor="nw", text="Patient Name", fill="#333333", font=("Montserrat Bold", 12))
        self.canvas.create_text(270, 110, anchor="nw", text="Phone", fill="#333333", font=("Montserrat Bold", 12))
        self.canvas.create_text(380, 110, anchor="nw", text="Date", fill="#333333", font=("Montserrat Bold", 12))
        self.canvas.create_text(520, 110, anchor="nw", text="Status", fill="#333333", font=("Montserrat Bold", 12))
        self.canvas.create_text(620, 110, anchor="nw", text="Select", fill="#333333", font=("Montserrat Bold", 12))

        # Create a dictionary to store appointment selection buttons
        self.selection_buttons = {}
        
        # Load appointments
        self.load_appointments()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Update the scrollregion to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.scrollable_frame_window, width=700)

    def load_appointments(self):
        # Clear existing appointments
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.selection_buttons = {}
        
        # Get appointments from database
        appointments = get_all_appointments()
        
        if not appointments:
            # Display message if no appointments
            label = Frame(self.scrollable_frame, bg="#f0f0f0", height=30)
            label.pack(fill="x", pady=5)
            Canvas(label, bg="#f0f0f0", height=30, width=700, bd=0, highlightthickness=0).create_text(
                350, 15, text="No appointments found", fill="#666666", font=("Montserrat", 12)
            )
            return
        
        # Create a row for each appointment
        for i, appt in enumerate(appointments):
            row_color = "#ffffff" if i % 2 == 0 else "#f5f5f5"
            row = Frame(self.scrollable_frame, bg=row_color, height=40)
            row.pack(fill="x", pady=1)
            
            # Create canvas for this row
            row_canvas = Canvas(row, bg=row_color, height=40, width=700, bd=0, highlightthickness=0)
            row_canvas.pack(fill="both")
            
            # Format appointment date
            date_str = appt[6].strftime("%Y-%m-%d %H:%M") if appt[6] else "N/A"
            
            # Add appointment info to row
            row_canvas.create_text(10, 20, anchor="w", text=str(appt[0]), fill="#000000", font=("Montserrat", 11))
            row_canvas.create_text(60, 20, anchor="w", text=appt[1][:20], fill="#000000", font=("Montserrat", 11))
            row_canvas.create_text(230, 20, anchor="w", text=appt[2], fill="#000000", font=("Montserrat", 11))
            row_canvas.create_text(340, 20, anchor="w", text=date_str, fill="#000000", font=("Montserrat", 11))
            
            # Add status with appropriate color
            status_color = "#4CAF50" if appt[7] == "Approved" else "#FF5722" if appt[7] == "Rejected" else "#2196F3"
            row_canvas.create_text(480, 20, anchor="w", text=appt[7], fill=status_color, font=("Montserrat Bold", 11))
            
            # Add select button
            select_btn = Button(
                row_canvas, 
                text="Select", 
                bg="#E0E0E0",
                fg="#000000",
                relief="flat",
                cursor="hand2",
                command=lambda id=appt[0]: self.select_appointment(id)
            )
            select_btn.place(x=580, y=10, width=60, height=25)
            
            # Store button reference
            self.selection_buttons[appt[0]] = select_btn

    def search_appointments(self):
        # You can implement search functionality here
        search_term = self.entry_1.get().strip().lower()
        
        if not search_term:
            # If search term is empty, just reload all appointments
            self.load_appointments()
            return
            
        # For now, just reload all appointments
        # In a real implementation, you would filter the appointments based on the search term
        self.load_appointments()
        messagebox.showinfo("Search", f"Searching for: {search_term}")
    
    def refresh_appointments(self):
        self.load_appointments()
        self.selected_appointment_id = None
        messagebox.showinfo("Refresh", "Appointments refreshed successfully")
    
    def select_appointment(self, appointment_id):
        # Reset previous selection
        if self.selected_appointment_id in self.selection_buttons:
            self.selection_buttons[self.selected_appointment_id].config(bg="#E0E0E0", text="Select")
        
        # Set new selection
        self.selected_appointment_id = appointment_id
        self.selection_buttons[appointment_id].config(bg="#4CAF50", text="Selected", fg="white")
    
    def approve_selected_appointment(self):
        if not self.selected_appointment_id:
            messagebox.showerror("Error", "Please select an appointment first")
            return
        
        try:
            update_appointment_status(self.selected_appointment_id, "Approved")
            messagebox.showinfo("Success", f"Appointment #{self.selected_appointment_id} approved successfully")
            self.refresh_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve appointment: {str(e)}")
    
    def delete_selected_appointment(self):
        if not self.selected_appointment_id:
            messagebox.showerror("Error", "Please select an appointment first")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete appointment #{self.selected_appointment_id}?")
        if not confirm:
            return
            
        try:
            delete_appointment(self.selected_appointment_id)
            messagebox.showinfo("Success", f"Appointment #{self.selected_appointment_id} deleted successfully")
            self.refresh_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete appointment: {str(e)}")
    
    def view_appointment_details(self):
        if not self.selected_appointment_id:
            messagebox.showerror("Error", "Please select an appointment first")
            return
            
        try:
            appt = get_appointment_details(self.selected_appointment_id)
            if appt:
                # Format date
                date_str = appt[6].strftime("%Y-%m-%d %H:%M") if appt[6] else "N/A"
                
                # Show details in a message box
                details = (
                    f"Appointment ID: {appt[0]}\n"
                    f"Patient Name: {appt[1]}\n"
                    f"Phone: {appt[2]}\n"
                    f"Address: {appt[3]}\n"
                    f"Gender: {appt[4]}\n"
                    f"Age: {appt[5]}\n"
                    f"Date: {date_str}\n"
                    f"Status: {appt[7]}"
                )
                messagebox.showinfo(f"Appointment #{appt[0]} Details", details)
            else:
                messagebox.showerror("Error", f"Appointment #{self.selected_appointment_id} not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve appointment details: {str(e)}")