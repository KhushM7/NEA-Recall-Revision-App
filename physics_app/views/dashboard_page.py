import customtkinter as ctk
from tkinter import StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from calendar import monthrange
from datetime import datetime
from matplotlib.dates import DateFormatter, DayLocator


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color="white")
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.user_id = user_id
        self.review_data = {}  # Initialize review data as empty
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        title_font = ctk.CTkFont(size=30, weight="bold")
        title_label = ctk.CTkLabel(
            self, text="Dashboard", font=title_font, text_color="black"
        )
        title_label.grid(row=0, column=1)

        # Create Frames
        self.create_frames()

    def create_frames(self):
        frame_colors = [
            "#FFB3B3",
            "#FFD9B3",
            "#FFFFB3",
            "#B3FFB3",
            "#B3D9FF",
            "#D9B3FF",
        ]

        frame_container = ctk.CTkFrame(self, fg_color="transparent")
        frame_container.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )
        frame_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        frame_container.grid_rowconfigure((0, 1), weight=1, uniform="row")

        for i in range(6):
            row, col = divmod(i, 3)
            frame = ctk.CTkFrame(
                frame_container, fg_color=frame_colors[i], corner_radius=10
            )
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            if i == 0:
                self.setup_review_log_frame(frame)
            else:
                ctk.CTkLabel(frame, text=f"Frame {i+1}", text_color="white").pack(
                    expand=True, padx=5, pady=5
                )

    def setup_review_log_frame(self, frame):
        title_font = ctk.CTkFont(size=16, weight="bold")
        ctk.CTkLabel(frame, text="Review Log", font=title_font).pack(pady=(10, 5))

        # Dropdowns for selecting month and year
        self.month_var = StringVar(value=datetime.now().strftime("%B"))
        self.year_var = StringVar(value=str(datetime.now().year))

        months = [datetime(2000, i, 1).strftime("%B") for i in range(1, 13)]
        years = [str(year) for year in range(2000, datetime.now().year + 1)]

        dropdown_frame = ctk.CTkFrame(frame, fg_color="transparent")
        dropdown_frame.pack(pady=(0, 10))

        ctk.CTkLabel(dropdown_frame, text="Month:").grid(row=0, column=0, padx=5)
        ctk.CTkOptionMenu(
            dropdown_frame,
            values=months,
            variable=self.month_var,
            command=self.update_graph,
        ).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(dropdown_frame, text="Year:").grid(row=0, column=2, padx=5)
        ctk.CTkOptionMenu(
            dropdown_frame,
            values=years,
            variable=self.year_var,
            command=self.update_graph,
        ).grid(row=0, column=3, padx=5)

        # Graph placeholder
        self.graph_canvas = ctk.CTkFrame(frame, fg_color="white", corner_radius=10)
        self.graph_canvas.pack(expand=True, fill="both", padx=10, pady=10)

        # Statistics below the graph
        self.stats_label = ctk.CTkLabel(frame, text="", wraplength=300, justify="left")
        self.stats_label.pack(pady=(10, 10))

        self.update_graph()

    def update_graph(self, *args):
        selected_month = self.month_var.get()
        selected_year = int(self.year_var.get())

        # Fetch data using flashcard_handler
        try:
            self.review_data = self.flashcard_handler.get_review_log_by_month(
                self.user_id, selected_month, selected_year
            )
        except Exception as e:
            print(f"Error fetching data: {str(e)}", text_color="red")
            return

        if not self.review_data:
            self.stats_label.configure(text="There were no reviews this month.")
            return

        # Generate graph with current review data
        self.plot_graph(selected_month, selected_year, self.review_data)

    def plot_graph(self, selected_month, selected_year, data_dict):
        # Get the month number and number of days in the selected month and year
        month_number = datetime.strptime(selected_month, "%B").month
        num_days = monthrange(selected_year, month_number)[1]

        # Generate a full list of days for the month (from 1st to the last day of the month)
        full_days = [
            datetime(selected_year, month_number, day) for day in range(1, num_days + 1)
        ]

        # Map reviews to the full days, filling missing days with 0 reviews
        day_to_review = {
            datetime(selected_year, month_number, int(day)): count
            for day, count in data_dict.items()
        }
        reviews_with_gaps = [day_to_review.get(day, 0) for day in full_days]

        # Create Matplotlib bar chart
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

        # Plot the bars with proper alignment
        ax.bar(full_days, reviews_with_gaps, color="skyblue", width=0.8)
        ax.set_title(f"Reviews in {selected_month} {selected_year}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Reviews")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Set the x-axis to show dates from 1st to the last day of the month
        ax.set_xlim([full_days[0], full_days[-1]])
        ax.xaxis.set_major_locator(DayLocator(interval=1))
        ax.xaxis.set_major_formatter(DateFormatter("%d"))

        # Make x-axis labels straight
        for label in ax.get_xticklabels():
            label.set_rotation(0)
            label.set_horizontalalignment("center")

        # Display graph on tkinter canvas
        for widget in self.graph_canvas.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        # Calculate stats
        most_reviewed_day = max(data_dict, key=data_dict.get)
        total_review_days = sum(1 for count in data_dict.values() if count > 0)
        self.stats_label.configure(
            text=f"Most Reviewed Day: {most_reviewed_day}\nTotal Review Days: {total_review_days}"
        )
