# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar, OptionMenu, ttk, messagebox, Scrollbar, Label
from controller import add_inventory_item, get_inventory_items, update_inventory_quantity, delete_inventory_item, get_inventory_categories


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def inventory():
    Inventory()

class Inventory(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg="#F9E6EE")

        # Main canvas
        self.canvas = Canvas(
            self,
            bg="#F9E6EE",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background image
        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(408.0, 226.0, image=self.image_1)
        
        # Title
        self.canvas.create_text(
            40, 20,
            anchor="nw",
            text="Inventory Management",
            fill="#000000",
            font=("Montserrat Bold", 20)
        )
        
        # Divider line
        self.canvas.create_rectangle(40, 60, 757, 62, fill="#DDDDDD", outline="")
        
        # Add new item frame
        self.add_item_frame = Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        self.add_item_frame.place(x=40, y=70, width=350, height=280)
        
        # Add item title
        Label(self.add_item_frame, text="Add New Item", font=("Montserrat Bold", 14), bg="#FFFFFF").place(x=10, y=10)
        
        # Category dropdown
        Label(self.add_item_frame, text="Category:", font=("Montserrat", 10), bg="#FFFFFF").place(x=10, y=50)
        self.category_var = StringVar()
        
        # Get categories or use defaults if can't connect to DB
        try:
            categories = get_inventory_categories()
            if not categories:
                categories = ["Medicines", "Equipment", "Syringes", "Surgical", "Patient Care", "Baby Kit"]
        except:
            categories = ["Medicines", "Equipment", "Syringes", "Surgical", "Patient Care", "Baby Kit"]
            
        self.category_var.set(categories[0] if categories else "Medicines")
        self.category_menu = ttk.Combobox(self.add_item_frame, textvariable=self.category_var, values=categories)
        self.category_menu.place(x=120, y=50, width=200)
        
        # Item name
        Label(self.add_item_frame, text="Item Name:", font=("Montserrat", 10), bg="#FFFFFF").place(x=10, y=90)
        self.name_entry = Entry(self.add_item_frame, font=("Montserrat", 10))
        self.name_entry.place(x=120, y=90, width=200)
        
        # Quantity
        Label(self.add_item_frame, text="Quantity:", font=("Montserrat", 10), bg="#FFFFFF").place(x=10, y=130)
        self.quantity_entry = Entry(self.add_item_frame, font=("Montserrat", 10))
        self.quantity_entry.place(x=120, y=130, width=200)
        
        # Price
        Label(self.add_item_frame, text="Unit Price ($):", font=("Montserrat", 10), bg="#FFFFFF").place(x=10, y=170)
        self.price_entry = Entry(self.add_item_frame, font=("Montserrat", 10))
        self.price_entry.place(x=120, y=170, width=200)
        
        # Add item button
        self.add_button = Button(
            self.add_item_frame,
            text="Add to Inventory",
            font=("Montserrat Bold", 10),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.add_item
        )
        self.add_button.place(x=120, y=220, width=150, height=35)
        
        # Clear form button
        self.clear_button = Button(
            self.add_item_frame,
            text="Clear Form",
            font=("Montserrat", 9),
            bg="#F5F5F5",
            relief="flat",
            cursor="hand2",
            command=self.clear_form
        )
        self.clear_button.place(x=280, y=220, width=60, height=35)
        
        # Inventory table frame
        self.inventory_frame = Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        self.inventory_frame.place(x=400, y=70, width=357, height=280)
        
        # Inventory title and search
        Label(self.inventory_frame, text="Current Inventory", font=("Montserrat Bold", 14), bg="#FFFFFF").place(x=10, y=10)
        
        # Refresh button
        self.refresh_button = Button(
            self.inventory_frame,
            text="Refresh",
            font=("Montserrat", 9),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.refresh_inventory
        )
        self.refresh_button.place(x=280, y=10, width=67, height=25)
        
        # Create the treeview for inventory items
        self.create_treeview()
        
        # Add buttons at bottom
        self.delete_button = Button(
            self,
            text="Delete Selected",
            font=("Montserrat Bold", 10),
            bg="#F44336",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.delete_selected
        )
        self.delete_button.place(x=647, y=360, width=150, height=35)
        
        # Update quantity button
        self.update_button = Button(
            self,
            text="Update Quantity",
            font=("Montserrat Bold", 10),
            bg="#FFC107",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.update_selected
        )
        self.update_button.place(x=487, y=360, width=150, height=35)
        
        # Load inventory data
        self.refresh_inventory()
        
    def create_treeview(self):
        """Create the treeview widget to display inventory items"""
        # Create a frame for the treeview with a scrollbar
        tree_frame = Frame(self.inventory_frame)
        tree_frame.place(x=10, y=45, width=337, height=225)
        
        # Create scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        
        # Create the treeview
        self.inventory_tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scroll.set,
            selectmode="browse"
        )
        
        # Configure the scrollbar
        tree_scroll.config(command=self.inventory_tree.yview)
        
        # Format the treeview
        self.inventory_tree["columns"] = ("ID", "Category", "Name", "Qty", "Price")
        self.inventory_tree.column("#0", width=0, stretch=False)
        self.inventory_tree.column("ID", width=30, anchor="center")
        self.inventory_tree.column("Category", width=80, anchor="w")
        self.inventory_tree.column("Name", width=100, anchor="w")
        self.inventory_tree.column("Qty", width=40, anchor="center")
        self.inventory_tree.column("Price", width=50, anchor="e")
        
        # Create headings
        self.inventory_tree.heading("#0", text="")
        self.inventory_tree.heading("ID", text="ID")
        self.inventory_tree.heading("Category", text="Category")
        self.inventory_tree.heading("Name", text="Item Name")
        self.inventory_tree.heading("Qty", text="Qty")
        self.inventory_tree.heading("Price", text="Price")
        
        # Place the treeview in the frame
        self.inventory_tree.pack(fill="both", expand=True)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Montserrat", 9))
        style.configure("Treeview.Heading", font=("Montserrat Bold", 9))
        
    def refresh_inventory(self):
        """Refresh the inventory data display"""
        # Clear existing data
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)
            
        try:
            # Get inventory data from database
            inventory_items = get_inventory_items()
            
            # Add items to the treeview
            for item in inventory_items:
                item_id, category, name, quantity, price, _ = item
                
                # Format price
                price_str = f"${price:.2f}" if price else "N/A"
                
                # Add to treeview
                self.inventory_tree.insert(
                    "",
                    "end",
                    values=(item_id, category, name, quantity, price_str)
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory data: {str(e)}")
    
    def add_item(self):
        """Add a new item to the inventory"""
        # Get form data
        category = self.category_var.get()
        name = self.name_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        # Validate inputs
        if not category:
            messagebox.showerror("Error", "Please select a category")
            return
            
        if not name:
            messagebox.showerror("Error", "Please enter an item name")
            return
            
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                messagebox.showerror("Error", "Quantity must be a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return
            
        try:
            price = float(price_str) if price_str else 0.0
            if price < 0:
                messagebox.showerror("Error", "Price must be a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return
            
        try:
            # Add to database
            add_inventory_item(category, name, quantity, price)
            messagebox.showinfo("Success", f"Item '{name}' added to inventory successfully")
            
            # Clear form and refresh display
            self.clear_form()
            self.refresh_inventory()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    def clear_form(self):
        """Clear the add item form"""
        self.name_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        
    def delete_selected(self):
        """Delete the selected inventory item"""
        # Get selected item
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an item to delete")
            return
            
        # Get the item ID from the selected row
        item_id = self.inventory_tree.item(selection, "values")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this item?")
        if not confirm:
            return
            
        try:
            # Delete from database
            delete_inventory_item(item_id)
            messagebox.showinfo("Success", f"Item deleted successfully")
            
            # Refresh display
            self.refresh_inventory()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {str(e)}")
    
    def update_selected(self):
        """Update the quantity of the selected inventory item"""
        # Get selected item
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an item to update")
            return
            
        # Get the item details from the selected row
        item_values = self.inventory_tree.item(selection, "values")
        item_id = item_values[0]
        item_name = item_values[2]
        current_qty = item_values[3]
        
        # Create update dialog
        update_window = Tk()
        update_window.title("Update Quantity")
        update_window.geometry("300x150")
        update_window.resizable(False, False)
        update_window.grab_set()  # Make window modal
        
        # Center on screen
        update_window.withdraw()
        update_window.update_idletasks()
        x = (update_window.winfo_screenwidth() - 300) // 2
        y = (update_window.winfo_screenheight() - 150) // 2
        update_window.geometry(f"300x150+{x}+{y}")
        update_window.deiconify()
        
        # Add widgets to update window
        Label(update_window, text=f"Update Quantity for: {item_name}", font=("Montserrat Bold", 10)).pack(pady=(10, 5))
        
        # Current quantity
        Label(update_window, text=f"Current Quantity: {current_qty}", font=("Montserrat", 9)).pack(pady=5)
        
        # New quantity entry
        Label(update_window, text="New Quantity:", font=("Montserrat", 9)).pack(pady=(5, 0))
        new_qty_entry = Entry(update_window, font=("Montserrat", 10))
        new_qty_entry.insert(0, current_qty)
        new_qty_entry.pack(pady=5)
        
        # Button frame
        button_frame = Frame(update_window)
        button_frame.pack(pady=10)
        
        # Cancel button
        Button(
            button_frame,
            text="Cancel",
            font=("Montserrat", 9),
            bg="#F5F5F5",
            width=10,
            command=update_window.destroy
        ).pack(side="left", padx=5)
        
        # Update button
        Button(
            button_frame,
            text="Update",
            font=("Montserrat Bold", 9),
            bg="#4CAF50",
            fg="white",
            width=10,
            command=lambda: self.process_quantity_update(item_id, new_qty_entry.get(), update_window)
        ).pack(side="left", padx=5)
        
    def process_quantity_update(self, item_id, new_qty_str, window):
        """Process the quantity update for an inventory item"""
        try:
            new_qty = int(new_qty_str)
            if new_qty < 0:
                messagebox.showerror("Error", "Quantity must be a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return
            
        try:
            # Update in database
            update_inventory_quantity(item_id, new_qty)
            messagebox.showinfo("Success", "Quantity updated successfully")
            
            # Close window and refresh
            window.destroy()
            self.refresh_inventory()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update quantity: {str(e)}")

# For standalone testing
if __name__ == "__main__":
    root = Tk()
    root.geometry("800x500")
    app = Inventory(root)
    app.pack(fill="both", expand=True)
    root.mainloop()