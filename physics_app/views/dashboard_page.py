import customtkinter as ctk
from tkinter import StringVar
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from datetime import datetime


def plot_calender_bar_graph(
    parent, selected_month, selected_year, data_dict, canvas_width, canvas_height
):
    """
    Generates and displays a graph in the specified parent frame.

    Args:
        parent: The frame where the graph should be displayed.
        selected_month: Name of the selected month.
        selected_year: Selected year as an integer.
        data_dict: Dictionary with day numbers as keys and review counts as values.
        canvas_width: Width of the canvas.
        canvas_height: Height of the canvas.
    """
    from calendar import monthrange
    from datetime import datetime
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter, DayLocator
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    # Create Matplotlib bar chart with the size of the canvas
    fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)

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
    for widget in parent.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


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
            frame.grid_rowconfigure(2, weight=1)
            frame.grid_rowconfigure(3, weight=0)
            if i == 0:
                self.setup_review_log_frame(frame)
            elif i == 5:  # Frame 6
                self.setup_future_reviews_frame(frame)
            else:
                ctk.CTkLabel(frame, text=f"Frame {i+1}", text_color="white").grid(
                    row=0, column=0, sticky="nsew", padx=5, pady=5
                )

    def setup_review_log_frame(self, frame):
        title_font = ctk.CTkFont(size=16, weight="bold")
        ctk.CTkLabel(frame, text="Review Log", font=title_font).grid(
            row=0, column=0, pady=(10, 5)
        )

        # Dropdowns for selecting month and year
        self.month_var = StringVar(value=datetime.now().strftime("%B"))
        self.year_var = StringVar(value=str(datetime.now().year))

        months = [datetime(2000, i, 1).strftime("%B") for i in range(1, 13)]
        years = [str(year) for year in range(2000, datetime.now().year + 1)]

        dropdown_frame = ctk.CTkFrame(frame, fg_color="transparent")
        dropdown_frame.grid(row=1, column=0, pady=(0, 10))

        ctk.CTkLabel(dropdown_frame, text="Month:").grid(row=0, column=0, padx=5)
        ctk.CTkOptionMenu(
            dropdown_frame,
            values=months,
            variable=self.month_var,
            command=self.update_review_log_graph,
        ).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(dropdown_frame, text="Year:").grid(row=0, column=2, padx=5)
        ctk.CTkOptionMenu(
            dropdown_frame,
            values=years,
            variable=self.year_var,
            command=self.update_review_log_graph,
        ).grid(row=0, column=3, padx=5)

        # Graph placeholder
        self.graph_canvas = ctk.CTkFrame(frame, fg_color="white", corner_radius=10)
        self.graph_canvas.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Statistics below the graph
        self.stats_label = ctk.CTkLabel(frame, text="", wraplength=300, justify="left")
        self.stats_label.grid(row=3, column=0, pady=0)

        self.update_review_log_graph()

    def update_review_log_graph(self, *args):
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
        else:
            most_reviewed_day = max(self.review_data, key=self.review_data.get)
            total_review_days = sum(
                1 for count in self.review_data.values() if count > 0
            )
            self.stats_label.configure(
                text=f"Most Reviewed Day: {most_reviewed_day}           Total Review Days: {total_review_days}"
            )

        # Get the dimensions of the graph canvas
        canvas_width = self.graph_canvas.winfo_width()
        canvas_height = self.graph_canvas.winfo_height()

        # Generate graph with current review data
        plot_calender_bar_graph(
            self.graph_canvas,
            selected_month,
            selected_year,
            self.review_data,
            canvas_width,
            canvas_height,
        )

    def setup_future_reviews_frame(self, frame):
        title_font = ctk.CTkFont(size=16, weight="bold")
        ctk.CTkLabel(frame, text="Future Reviews", font=title_font).grid(
            row=0, column=0, pady=(10, 5), columnspan=3
        )

        # Initialize the month and year variables
        self.future_month_var = StringVar(value=datetime.now().strftime("%B"))
        self.future_year_var = StringVar(value=str(datetime.now().year))

        # Placeholder test dictionary
        self.test_data = {day: day * 2 for day in range(1, 32)}  # Example data

        # Calendar canvas
        self.calendar_canvas = ctk.CTkFrame(frame, fg_color="white", corner_radius=10)
        self.calendar_canvas.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )

        # Navigation buttons
        prev_button = ctk.CTkButton(
            frame, text="Prev", command=self.show_previous_month
        )
        prev_button.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        next_button = ctk.CTkButton(frame, text="Next", command=self.show_next_month)
        next_button.grid(row=2, column=2, sticky="e", padx=10, pady=10)

        # Stats label
        self.future_stats_label = ctk.CTkLabel(
            frame, text="Total Cards to Review: ", wraplength=300, justify="left"
        )
        self.future_stats_label.grid(row=3, column=0, columnspan=3, pady=(10, 10))

        # Configure frame rows and columns
        frame.grid_rowconfigure(1, weight=1)  # Calendar takes up most of the space
        frame.grid_columnconfigure(1, weight=1)

        # Initial rendering of the calendar
        self.update_future_calendar()

    def update_future_calendar(self):
        # Fetch month and year
        selected_month = self.future_month_var.get()
        selected_year = int(self.future_year_var.get())

        # Generate total cards to review (sum of the test dictionary values)
        total_cards = sum(self.test_data.values())
        self.future_stats_label.configure(text=f"Total Cards to Review: {total_cards}")

        # Get the dimensions of the calendar canvas
        canvas_width = self.calendar_canvas.winfo_width() or 600  # Default width
        canvas_height = self.calendar_canvas.winfo_height() or 400  # Default height

        # Render the calendar graph
        plot_calender_bar_graph(
            self.calendar_canvas,
            selected_month,
            selected_year,
            self.test_data,
            canvas_width,
            canvas_height,
        )

    def show_previous_month(self):
        # Move to the previous month
        current_month = datetime.strptime(self.future_month_var.get(), "%B").month
        current_year = int(self.future_year_var.get())

        if current_month == 1:  # If January, move to December of the previous year
            new_month = 12
            new_year = current_year - 1
        else:
            new_month = current_month - 1
            new_year = current_year

        self.future_month_var.set(datetime(2000, new_month, 1).strftime("%B"))
        self.future_year_var.set(str(new_year))
        self.update_future_calendar()

    def show_next_month(self):
        # Move to the next month
        current_month = datetime.strptime(self.future_month_var.get(), "%B").month
        current_year = int(self.future_year_var.get())

        if current_month == 12:  # If December, move to January of the next year
            new_month = 1
            new_year = current_year + 1
        else:
            new_month = current_month + 1
            new_year = current_year

        self.future_month_var.set(datetime(2000, new_month, 1).strftime("%B"))
        self.future_year_var.set(str(new_year))
        self.update_future_calendar()
