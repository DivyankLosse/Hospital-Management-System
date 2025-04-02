from pathlib import Path
from tkinter.constants import ANCHOR, N
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, N, Label
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def dashboard():
    Dashboard()

class Dashboard(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#F9E6EE")

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
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            398.0,
            216.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(
            112.0,
            92.0,
            image=self.image_image_2
        )

        # Get real appointment statistics
        try:
            stats = db_controller.get_appointment_stats()
            total_appointments_count = stats['total']
            pending_count = stats['pending']
            completed_count = stats['completed']
            cancelled_count = stats['cancelled']
        except Exception as e:
            # Fallback to dummy values if there's an error
            total_appointments_count = 82
            pending_count = 30
            completed_count = 40
            cancelled_count = 12

        # Display total appointments count
        self.total_count_text = self.canvas.create_text(
            81.0,
            70.0,
            anchor="nw",
            text=str(total_appointments_count),
            fill="#000000",
            font=("Montserrat Bold", 48 * -1)
        )

        self.image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(
            476.0,
            92.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(
            294.0,
            92.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(
            658.0,
            92.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=relative_to_assets("image_6.png"))
        image_6 = self.canvas.create_image(
            205.0,
            278.0,
            image=self.image_image_6
        )

        self.image_image_7 = PhotoImage(
            file=relative_to_assets("image_7.png"))
        image_7 = self.canvas.create_image(
            567.0,
            278.0,
            image=self.image_image_7
        )

        self.canvas.create_text(
            85.0,
            54.0,
            anchor="nw",
            text="Total\n",
            fill="#676666",
            font=("Montserrat Bold", 20 * -1)
        )

        self.canvas.create_text(
            264.0,
            55.0,
            anchor="nw",
            text="Pending",
            fill="#676666",
            font=("Montserrat Bold", 20 * -1)
        )

        self.canvas.create_text(
            439.0,
            52.0,
            anchor="nw",
            text="Completed",
            fill="#676666",
            font=("Montserrat Bold", 20 * -1)
        )

        self.canvas.create_text(
            597.0,
            55.0,
            anchor="nw",
            text="Cancelled",
            fill="#676666",
            font=("Montserrat Bold", 20 * -1)
        )

        # Pending appointments count (was OPD)
        self.pending_count_text = self.canvas.create_text(
            264.0,
            76.0,
            anchor="nw",
            text=str(pending_count),
            fill="#000000",
            font=("Montserrat Bold", 48 * -1)
        )

        # Completed appointments count (was Direct)
        self.completed_count_text = self.canvas.create_text(
            447.0,
            76.0,
            anchor="nw",
            text=str(completed_count),
            fill="#000000",
            font=("Montserrat Bold", 48 * -1)
        )

        # Cancelled appointments count (was Pre-Booked)
        self.cancelled_count_text = self.canvas.create_text(
            628.0,
            74.0,
            anchor="nw",
            text=str(cancelled_count),
            fill="#000000",
            font=("Montserrat Bold", 48 * -1)
        )

        self.canvas.create_text(
            56.0,
            187.0,
            anchor="nw",
            text="Status",
            fill="#676666",
            font=("Montserrat Bold", 24 * -1)
        )

        self.image_image_9 = PhotoImage(
            file=relative_to_assets("image_9.png"))
        image_9 = self.canvas.create_image(
            309.0,
            218.0,
            image=self.image_image_9
        )

        self.image_image_10 = PhotoImage(
            file=relative_to_assets("image_10.png"))
        image_10 = self.canvas.create_image(
            273.0,
            198.0,
            image=self.image_image_10
        )

        self.image_image_11 = PhotoImage(
            file=relative_to_assets("image_11.png"))
        image_11 = self.canvas.create_image(
            273.0,
            217.0,
            image=self.image_image_11
        )

        self.image_image_12 = PhotoImage(
            file=relative_to_assets("image_12.png"))
        image_12 = self.canvas.create_image(
            273.0,
            236.0,
            image=self.image_image_12
        )

        self.image_image_13 = PhotoImage(
            file=relative_to_assets("image_13.png"))
        image_13 = self.canvas.create_image(
            314.0,
            214.0,
            image=self.image_image_13
        )

        self.image_image_15 = PhotoImage(
            file=relative_to_assets("image_15.png"))
        image_15 = self.canvas.create_image(
            398.0,
            155.0,
            image=self.image_image_15
        )

        # Create refresh button
        self.refresh_button = Button(
            self,
            text="↻ Refresh",
            font=("Montserrat Bold", 10),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.refresh_stats
        )
        self.refresh_button.place(x=700, y=10, width=80, height=30)

        # Create the modern left chart (donut chart)
        self.create_appointment_status_chart(pending_count, completed_count, cancelled_count)
        
        # Create the modern right chart (stacked bar chart)
        self.create_appointment_trend_chart()

    def create_appointment_status_chart(self, pending, completed, cancelled):
        """Create a modern donut chart showing appointment status distribution"""
        # Frame to hold the chart
        chart_frame = Frame(self, bg="#FFFFFF", bd=0, highlightthickness=0)
        chart_frame.place(x=40, y=220, width=320, height=200)
        
        # Create figure for the chart
        fig = Figure(figsize=(3.2, 2.0), dpi=100)
        ax = fig.add_subplot(111)
        
        # Data and colors - ensure we don't have zero values that cause NaN errors
        sizes = [max(1, pending), max(1, completed), max(1, cancelled)]
        labels = ['Pending', 'Completed', 'Cancelled']
        colors = ['#2196F3', '#4CAF50', '#FF5722']
        explode = (0.05, 0.05, 0.05)  # explode all slices slightly
        
        # Set equal aspect ratio to make it a circle and set background color
        ax.set_aspect('equal')
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')
        
        # Create the donut chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            explode=explode,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor='w')
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
            autotext.set_color('white')
        
        # Add a title
        ax.set_title('Appointment Status', fontsize=12, pad=10)
        
        # Add a legend
        ax.legend(wedges, labels, loc="center", bbox_to_anchor=(0.5, 0),
                  frameon=False, ncol=3, fontsize=8)
        
        # Remove axis
        ax.axis('off')
        
        # Add the chart to the frame
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_appointment_trend_chart(self):
        """Create a modern stacked bar chart showing appointment trends"""
        # Frame to hold the chart
        chart_frame = Frame(self, bg="#FFFFFF", bd=0, highlightthickness=0)
        chart_frame.place(x=420, y=220, width=320, height=200)
        
        # Create figure for the chart
        fig = Figure(figsize=(3.2, 2.0), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sample data - in a real app, you would get this from your database
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        pending = [10, 15, 7, 10, 5]
        completed = [15, 18, 25, 20, 18]
        cancelled = [3, 5, 8, 4, 2]
        
        # Set background color
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F8F9FA')
        
        # Plot the stacked bars
        ax.bar(months, pending, label='Pending', color='#2196F3')
        ax.bar(months, completed, bottom=pending, label='Completed', color='#4CAF50')
        ax.bar(months, cancelled, bottom=[i+j for i,j in zip(pending, completed)], label='Cancelled', color='#FF5722')
        
        # Customize the chart
        ax.set_title('Monthly Trends', fontsize=12, pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#DDDDDD')
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.tick_params(axis='both', colors='#666666', labelsize=8)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color='#EEEEEE')
        
        # Add a legend
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False, fontsize=8)
        
        # Add the chart to the frame
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_stats(self):
        """Refresh appointment statistics"""
        try:
            # Get fresh stats from the database
            stats = db_controller.get_appointment_stats()
            total = stats['total']
            pending = stats['pending']
            completed = stats['completed']
            cancelled = stats['cancelled']
            
            # Update the displayed statistics
            self.canvas.itemconfig(self.total_count_text, text=str(total))
            self.canvas.itemconfig(self.pending_count_text, text=str(pending))
            self.canvas.itemconfig(self.completed_count_text, text=str(completed))
            self.canvas.itemconfig(self.cancelled_count_text, text=str(cancelled))
            
            # Re-create the charts with updated data
            try:
                self.create_appointment_status_chart(pending, completed, cancelled)
                self.create_appointment_trend_chart()
            except Exception as chart_err:
                print(f"Error creating charts: {chart_err}")
                # Continue even if charts fail
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            # If there's an error, we don't update the UI
            pass