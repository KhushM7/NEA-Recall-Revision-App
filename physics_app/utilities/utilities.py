from calendar import monthrange
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Tuple

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DayLocator, DateFormatter


def configure_grid(frame: ctk.CTkFrame, rows: int, columns: int) -> None:
    """Configures grid layout for a given frame.
    :rtype: object
    """
    for i in range(rows):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(columns):
        frame.grid_columnconfigure(i, weight=1)


def resize_and_update_image(
    image: Image.Image,
    canvas: ctk.CTkCanvas,
    canvas_size: Tuple[int, int],
    scale_factor: float = 1.5,
) -> None:
    """
    Resize an image to fit within the canvas size while maintaining aspect ratio,
    and update the canvas with the resized image.

    :param image: The original PIL Image to resize.
    :param canvas: The canvas widget to display the image.
    :param canvas_size: The size (width, height) of the canvas.
    :param scale_factor: Factor to scale down the width of the image.
    """
    width, height = canvas_size
    new_width = int(width / scale_factor)
    new_height = int((image.height / image.width) * new_width)

    if new_height > height:
        new_height = height
        new_width = int(new_height / (image.height / image.width))

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(resized_image)

    # Clear the canvas and update with the resized image
    canvas.delete("all")
    canvas.create_image(width // 2, height // 2, image=image_tk, anchor="center")

    # Keep a reference to avoid garbage collection
    canvas.image_tk = image_tk


def plot_histogram(
    parent,
    data_list,
    bins,
    canvas_width,
    canvas_height,
    graph_text,
    x_label,
    y_label,
):
    """
    Plots a histogram using the given data.

    Args:
        parent: Tkinter parent widget where the chart will be displayed.
        data_list: List of numerical data to plot in the histogram.
        bins: Number of bins for the histogram.
        canvas_width: Width of the canvas in pixels.
        canvas_height: Height of the canvas in pixels.
        graph_text: Title of the graph.
        x_label: Label for the x-axis.
        y_label: Label for the y-axis.
    """
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # Define a single color for all bins
    color = plt.cm.Paired(0)  # Choose the first color in the Paired colormap

    # Adjust figure size to fully utilize canvas space
    fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)

    # Create the histogram
    ax.hist(
        data_list,
        bins=bins,
        color=color,
        edgecolor="black",
        alpha=0.7,  # Transparency for better visual effect
    )

    # Dynamically adjust font sizes for the title and labels
    title_fontsize = max(canvas_height // 20, 14)
    label_fontsize = max(canvas_height // 35, 5)

    ax.set_title(
        graph_text,
        fontsize=title_fontsize,
        pad=canvas_height // 40,
    )
    ax.set_xlabel(
        x_label,
        fontsize=label_fontsize,
        labelpad=canvas_height // 50,
    )
    ax.set_ylabel(
        y_label,
        fontsize=label_fontsize,
        labelpad=canvas_height // 50,
    )

    # Adjust layout to ensure the graph fits within the canvas
    fig.tight_layout(pad=1.5)

    # Clear any existing widgets before displaying the new chart
    for widget in parent.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


def plot_calendar_bar_graph(
    parent,
    selected_month,
    selected_year,
    data_dict,
    canvas_width,
    canvas_height,
):
    month_number = datetime.strptime(selected_month, "%B").month
    num_days = monthrange(selected_year, month_number)[1]
    full_days = [
        datetime(selected_year, month_number, day) for day in range(1, num_days + 1)
    ]
    day_to_review = {
        datetime(selected_year, month_number, int(day)): count
        for day, count in data_dict.items()
    }
    reviews_with_gaps = [day_to_review.get(day, 0) for day in full_days]

    # Adjust figure to fit the available canvas
    fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)
    ax.bar(full_days, reviews_with_gaps, color="skyblue", width=0.8)
    ax.set_title(f"Reviews in {selected_month} {selected_year}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Reviews")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_xlim([full_days[0], full_days[-1]])
    ax.xaxis.set_major_locator(DayLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter("%d"))
    for label in ax.get_xticklabels():
        label.set_rotation(0)
        label.set_horizontalalignment("center")

    # Use tight layout to prevent clipping
    fig.tight_layout(pad=2)

    # Clear any existing widgets before displaying the new graph
    for widget in parent.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


def plot_pie_chart(
    parent,
    data_dict,
    canvas_width,
    canvas_height,
):
    # Extract keys and values from the data dictionary
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    # Define colors for each slice
    colors = plt.cm.Paired(range(len(labels)))

    # Adjust figure size to fully utilize canvas space
    fig, ax = plt.subplots(figsize=(canvas_width / 100, canvas_height / 100), dpi=100)

    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops={"fontsize": max(canvas_width // 50, 10)},  # Dynamic text size
    )

    # Ensure the pie chart is a perfect circle and fills the canvas
    ax.set_aspect("equal")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove all margins

    # Clear any existing widgets before displaying the new chart
    for widget in parent.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
